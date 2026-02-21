from __future__ import annotations


class StrategyEngine:
    def __init__(self):
        self._strategies = {}

    def register_strategy(self, strategy):
        self._strategies[strategy.name] = strategy

    def get_strategy(self, name):
        return self._strategies[name]

    def list_strategies(self):
        return list(self._strategies.keys())

    def evaluate_strategies(self, goal, context):
        return sorted([(n, s.is_suitable(goal, context)) for n, s in self._strategies.items()], key=lambda x: x[1], reverse=True)

    def select_strategy(self, goal, context):
        return self._strategies[self.evaluate_strategies(goal, context)[0][0]]
