class rules:
    def __init__(self, rule_id,data_category,condition,required_action):
        self.rule_id = rule_id
        self.data_category = data_category
        self.condition = condition
        self.required_action = required_action
        self.is_satisfied = False

    def __repr__(self):
        return f"rules(rule_id={self.rule_id}, data_category={self.data_category}, condition={self.condition}, required_action={self.required_action})"