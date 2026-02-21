from __future__ import annotations

from planning_system.models.constraint import Constraint, ConstraintType


class CustomConstraint:
    def __init__(self, name, check_function):
        self.name = name
        self.check_function = check_function



def create_custom_constraint(name, check_function):
    c = Constraint(constraint_type=ConstraintType.CUSTOM, name=name)
    c._fn = check_function
    return c
