class output_model:
    def __init__(self, case_id,deletion_status,steps_json):
        self.case_id = case_id
        self.deletion_status = deletion_status
        self.steps_json = steps_json

    def __repr__(self):
        return f"output_model(case_id={self.case_id}, deletion_status={self.deletion_status}, steps_json={self.steps_json})"
    