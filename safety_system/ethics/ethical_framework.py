class EthicalFramework:
    def __init__(self, principles, value_hierarchy, evaluator, resolver):
        self.principles = principles
        self.value_hierarchy = value_hierarchy
        self.evaluator = evaluator
        self.resolver = resolver

    def decide(self, action: str, context: dict) -> dict:
        return self.evaluator.evaluate(action, context)
