class ApprovalWorkflow:
    def format_request(self, action: str, description: str, risk_level: str, consequences: list[str]) -> str:
        return (
            f"I would like to {action}.\nThis will {', '.join(consequences) or 'have limited impact'}.\n"
            f"Risk level: {risk_level}.\nDo you approve? (yes/no)"
        )
