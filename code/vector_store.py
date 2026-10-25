import base64
import json
import tempfile
import time
from pathlib import Path

from openai import OpenAI

# File Search only indexes certain extensions; the others are converted to text first.
NATIVE_EXTENSIONS = {".pdf", ".txt", ".json", ".md"}
TEXT_AS_TXT_EXTENSIONS = {".sql", ".log"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}

STATE_FILE = Path(__file__).resolve().parent / "config" / "vector_store.json"
VECTOR_STORE_NAME = "ghost-data-evidence"
UPLOAD_RETRY_ATTEMPTS = 5


def _upload_name(path: Path, evidence_dir: Path) -> str:
    """Flatten the relative path so the manifest's file_path stays recoverable from the filename."""
    relative = path.relative_to(evidence_dir.parent).as_posix()
    return relative.replace("/", "__")


def _describe_image(client: OpenAI, model: str, path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": (
                    "Extract structured data from this image and return ONLY valid JSON.\n"
                    "Use this exact top-level structure:\n"
                    "{\n"
                    '  "category": "string",\n'
                    '  "user_id": "string",\n'
                    '  "account_id": "string",\n'
                    '  "email_id": "string",\n'
                    '  "data": [\n'
                    "    {\n"
                    '      "...other headers from the same row...": "value"\n'
                    "    }\n"
                    "  ]\n"
                    "}\n\n"
                    "Rules:\n"
                    "1) user_id must start with 'user_'.\n"
                    "2) account_id should be captured from the field next to user_id.\n"
                    "3) email_id should be captured from the field adjacent to account_id.\n"
                    "4) category must be decided from the image name and visible content.\n"
                    "5) If the image has a repetitive list/table, create one dictionary per row inside data[].\n"
                    "6) For each row dictionary, include column headers as keys and cell values as values.\n"
                    "7) If no table/list exists, keep data as a single-item array with available fields.\n"
                    "8) Do not return markdown or prose, JSON only.\n\n"
                    f"Image file name: {path.name}"
                )},
                {"type": "image_url", "image_url": {"url": f"data:image/{path.suffix[1:].lower()};base64,{encoded}"}},
            ],
        }],
    )
    return response.choices[0].message.content or "{}"


def _prepare_files(client: OpenAI, vision_model: str, evidence_dir: Path, staging: Path) -> list[Path]:
    prepared: list[Path] = []
    for path in sorted(p for p in evidence_dir.rglob("*") if p.is_file()):
        name = _upload_name(path, evidence_dir)
        suffix = path.suffix.lower()
        target = staging / name
        if suffix in NATIVE_EXTENSIONS:
            target.write_bytes(path.read_bytes())
        elif suffix in TEXT_AS_TXT_EXTENSIONS:
            target = staging / f"{name}.txt"
            target.write_text(path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        elif suffix in IMAGE_EXTENSIONS:
            target = staging / f"{name}.txt"
            target.write_text(_describe_image(client, vision_model, path), encoding="utf-8")
        else:
            print(f"Skipping unsupported evidence file: {path}")
            continue
        prepared.append(target)
    return prepared


def get_or_create_vector_store(client: OpenAI, evidence_dir: Path, vision_model: str) -> str:
    """Return the id of the shared evidence vector store, building it only on the first run."""
    if STATE_FILE.exists():
        stored_id = json.loads(STATE_FILE.read_text(encoding="utf-8")).get("vector_store_id")
        if stored_id:
            try:
                client.vector_stores.retrieve(stored_id)
                print(f"Reusing vector store {stored_id}")
                return stored_id
            except Exception as error:
                print(f"Stored vector store unusable ({error}); creating a new one")

    vector_store = client.vector_stores.create(
        name=VECTOR_STORE_NAME,
        expires_after={"anchor": "last_active_at", "days": 3},
    )
    with tempfile.TemporaryDirectory() as tmp:
        files = _prepare_files(client, vision_model, evidence_dir, Path(tmp))
        if not files:
            raise RuntimeError(f"No supported evidence files found in {evidence_dir}")

        batch = None
        last_error = None
        for attempt in range(1, UPLOAD_RETRY_ATTEMPTS + 1):
            handles = [open(f, "rb") for f in files]
            try:
                batch = client.vector_stores.file_batches.upload_and_poll(
                    vector_store_id=vector_store.id, files=handles
                )
                break
            except Exception as error:
                last_error = error
                wait_seconds = min(2 ** attempt, 30)
                print(
                    f"Vector store upload attempt {attempt}/{UPLOAD_RETRY_ATTEMPTS} failed: {error}. "
                    f"Retrying in {wait_seconds}s..."
                )
                if attempt < UPLOAD_RETRY_ATTEMPTS:
                    time.sleep(wait_seconds)
            finally:
                for handle in handles:
                    handle.close()

        if batch is None:
            try:
                client.vector_stores.delete(vector_store.id)
            except Exception as cleanup_error:
                print(f"Failed to clean up vector store {vector_store.id}: {cleanup_error}")
            raise RuntimeError(
                f"Failed to upload evidence to vector store after {UPLOAD_RETRY_ATTEMPTS} attempts."
            ) from last_error

    print(f"Vector store {vector_store.id}: {batch.file_counts.completed}/{len(files)} files indexed, "
          f"{batch.file_counts.failed} failed")
    STATE_FILE.write_text(json.dumps({"vector_store_id": vector_store.id}), encoding="utf-8")
    return vector_store.id


def ask_with_file_search(client: OpenAI, model: str, vector_store_id: str, instructions: str, question: str):
    """Send only the new question; relevant evidence chunks are retrieved server-side."""
    return client.responses.create(
        model=model,
        instructions=instructions,
        input=question,
        tools=[{"type": "file_search", "vector_store_ids": [vector_store_id], "max_num_results": 10}],
    )
