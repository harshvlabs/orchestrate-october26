class evidence_model:
    def __init__(self, file_id,file_path,origin,captured_at):
        self.file_id = file_id
        self.file_path = file_path
        self.origin = origin
        self.captured_at = captured_at

    def __repr__(self):
        return f"evidence_model(file_id={self.file_id}, file_path={self.file_path}, origin={self.origin}, captured_at={self.captured_at})"