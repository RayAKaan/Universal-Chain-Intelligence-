from __future__ import annotations


class RollbackError(Exception):
    pass


class RollbackManager:
    def __init__(self):
        self.checkpoints = {}

    def record_checkpoint(self, plan_id, step_id, state):
        self.checkpoints.setdefault(plan_id, []).append({"step_id": step_id, "state": state})

    def get_checkpoints(self, plan_id):
        return self.checkpoints.get(plan_id, [])

    def rollback_to(self, plan_id, checkpoint_step_id):
        cps = self.checkpoints.get(plan_id, [])
        return any(c["step_id"] == checkpoint_step_id for c in cps)

    def rollback_step(self, step, context):
        if not self.is_reversible(step):
            return False
        context.variables.pop(f"step:{step.step_id}:result", None)
        return True

    def is_reversible(self, step):
        return step.step_type.value in {"TRANSFORM", "CHECKPOINT"} or "save" not in step.name
