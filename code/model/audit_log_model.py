class audit_log:
    def __init__(self, audit_id,user_id,event_time,field_name,old_value,new_value):
        self.audit_id = audit_id
        self.user_id = user_id
        self.event_time = event_time
        self.field_name = field_name
        self.old_value = old_value
        self.new_value = new_value

    def __repr__(self):
        return f"audit_log(audit_id={self.audit_id}, user_id={self.user_id}, event_time={self.event_time}, field_name={self.field_name}, old_value={self.old_value}, new_value={self.new_value})"