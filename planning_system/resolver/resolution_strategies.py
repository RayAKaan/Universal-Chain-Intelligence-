from __future__ import annotations

from planning_system.resolver.match_scoring import calculate_match_score, string_similarity


class ExactMatchStrategy:
    def score(self, step, cap):
        return 1.0 if step.name.lower() == cap.name.lower() else 0.0


class FuzzyMatchStrategy:
    def score(self, step, cap):
        return string_similarity(step.name, cap.name)


class CategoryMatchStrategy:
    def score(self, step, cap):
        return 1.0 if cap.category in step.description.lower() else 0.3


class CompositeMatchStrategy:
    def __init__(self):
        self.exact = ExactMatchStrategy()
        self.fuzzy = FuzzyMatchStrategy()
        self.category = CategoryMatchStrategy()

    def score(self, step, cap):
        return max(self.exact.score(step, cap), 0.6 * self.fuzzy.score(step, cap) + 0.4 * self.category.score(step, cap), calculate_match_score(step, cap))
