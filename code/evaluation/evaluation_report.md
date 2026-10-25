# Evaluation Report

This report summarizes evaluation quality for the final run that produced [output.csv](../output.csv).

## 1) Case-level deletion-status accuracy

- Total cases evaluated: **518**
- Correct `deletion_status` predictions: **TBD**
- Case-level accuracy: **TBD%**

## 2) Step-level and field-level accuracy

### 2.1 Step-level metrics

- Exact step match accuracy: **TBD%**
- Precision: **TBD**
- Recall: **TBD**
- F1 score: **TBD**

### 2.2 Field-level metrics

| Field | Accuracy |
|---|---|
| `step_no` | TBD |
| `phase` | TBD |
| `system_id` | TBD |
| `resource_id` | TBD |
| `operation` | TBD |
| `state` | TBD |
| `evidence_id` | TBD |

## 3) Sequence accuracy

- Exact ordered-sequence match per case: **TBD%**
- Notes: **TBD**

## 4) Additional participant-created evaluation cases

At least three custom cases are included below with expected behavior.

### Case A — Non-deletion request should be NOT_APPLICABLE

- Scenario: Request asks for data export only, not deletion.
- Expected output:
  - `deletion_status=NOT_APPLICABLE`
  - `steps_json=[]`

### Case B — Tombstone retention with identifier redaction

- Scenario: Account requires tombstone retention while direct identifiers must be removed.
- Expected output:
  - `deletion_status=COMPLETE` only if retained record is present and redacted per policy.
  - Verification includes `VERIFY_RECORD_PRESENT` and `VERIFY_RECORD_REDACTED` with valid evidence.

### Case C — Reported COMPLETE but restore risk remains

- Scenario: Workflow reports completion, but a backup restore path can recreate prohibited data at `audit_at`.
- Expected output:
  - `deletion_status=INCOMPLETE`
  - Findings include `REPORT_RESTORE_RISK` (`ACTIVE`) with evidence.
  - Remediation includes `BLOCK_RESTORE` before dependent cleanup verification.

## 5) Failures found and improvements made

### 5.1 Failures found

1. **TBD**
2. **TBD**
3. **TBD**

### 5.2 Improvements made

1. **TBD**
2. **TBD**
3. **TBD**

### 5.3 Final observations

- Determinism checks: **TBD**
- Remaining known gaps: **TBD / None**
