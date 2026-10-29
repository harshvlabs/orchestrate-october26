from model.audit_log_model import audit_log
import json

class user_identity:
    def __init__(self, user_id, name, email, phone, email_hash, updated_at):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.email_hash = email_hash
        self.updated_at = updated_at
        self.user_audit_logs: list[audit_log] = []
        

    def __repr__(self):
        return f"user_identity(user_id={self.user_id}, name={self.name}, email={self.email}, phone={self.phone}, email_hash={self.email_hash}, updated_at={self.updated_at})"

    def user_audit_logs_json(self):
        data = []
        for log in self.user_audit_logs:
            data.append({
                "audit_id": log.audit_id,
                "user_id": log.user_id,
                "event_time": log.event_time,
                "field_name": log.field_name,
                "old_value": log.old_value,
                "new_value": log.new_value,
            })
        return json.dumps(data, ensure_ascii=False)