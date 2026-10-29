from model.deletion_rule import rules

class deletion_request:
    def __init__(self, case_id,email,requested_at,reported_status,reported_at,audit_at,request_text):
        self.case_id = case_id
        self.email = email
        self.requested_at = requested_at
        self.reported_status = reported_status
        self.reported_at = reported_at
        self.audit_at = audit_at
        self.request_text = request_text
        self.is_deletion_requested = True
        self.request_rules: list[rules] = []

    def __repr__(self):
        return f"deletion_request(case_id={self.case_id}, email={self.email}, requested_at={self.requested_at}, reported_status={self.reported_status}, reported_at={self.reported_at}, audit_at={self.audit_at}, request_text={self.request_text}, is_deletion_requested={self.is_deletion_requested}, request_rules={self.request_rules})"