from __future__ import annotations

from construction_system.models.build_result import BuildResult, BuildStatus
from construction_system.models.recursive_task import RecursiveTask
from construction_system.recursive.recursive_context import RecursiveContext


class RecursiveExecutionEngine:
    def __init__(self, planning_engine, construction_manager, recursion_controller, context_manager, config):
        self.planning_engine = planning_engine
        self.construction_manager = construction_manager
        self.recursion_controller = recursion_controller
        self.context_manager = context_manager
        self.config = config

    def spawn_child_task(self, parent, child_spec):
        b = self.recursion_controller.allocate_budget(parent, 1)[0]
        child = RecursiveTask(
            parent_task_id=parent.task_id,
            root_task_id=parent.root_task_id or parent.task_id,
            name=child_spec.name,
            description=child_spec.description,
            specification=child_spec,
            depth=parent.depth + 1,
            max_depth=parent.max_depth,
            resource_budget=b,
        )
        parent.child_task_ids.append(child.task_id)
        return child

    def collect_results(self, parent, child_results):
        out = BuildResult(spec_id=parent.specification.spec_id if parent.specification else "", status=BuildStatus.SUCCESS)
        for r in child_results:
            out.files_created += r.files_created
            out.artifacts_created += r.artifacts_created
            out.components_built += r.components_built
            out.errors += r.errors
        if out.errors:
            out.status = BuildStatus.PARTIAL_SUCCESS
        return out

    def execute_recursive(self, task):
        if self.recursion_controller.check_cycle(task, task.specification):
            return BuildResult(spec_id=task.specification.spec_id, status=BuildStatus.FAILURE, errors=["cycle detected"])

        allowed, reason = self.recursion_controller.can_recurse(task)
        self.recursion_controller.record_task(task)
        if not allowed:
            return BuildResult(spec_id=task.specification.spec_id, status=BuildStatus.FAILURE, errors=[reason])

        context = RecursiveContext(
            root_task_id=task.root_task_id or task.task_id,
            current_depth=task.depth,
            max_depth=task.max_depth,
            resource_budget=task.resource_budget,
        )
        task.status = "running"
        parent_result = self.construction_manager.construct_direct(task.specification, context)
        children = self.construction_manager.subtask_generator.generate_subtasks(task.specification)
        if children and task.depth < task.max_depth:
            child_results = []
            for cs in children:
                c = self.spawn_child_task(task, cs)
                child_results.append(self.execute_recursive(c))
            agg = self.collect_results(task, child_results)
            agg.files_created = parent_result.files_created + agg.files_created
            return agg

        task.status = "completed"
        return parent_result

    def execute_with_planning(self, specification):
        try:
            goal_txt = f"Build {specification.name}"
            if self.planning_engine:
                self.planning_engine.execute_goal(goal_txt)
        except Exception:
            pass
        t = RecursiveTask(root_task_id="", name=specification.name, description=specification.description, specification=specification)
        t.root_task_id = t.task_id
        return self.execute_recursive(t)

    def get_execution_tree(self, root_task_id):
        return self.recursion_controller.get_task_tree(root_task_id)

    def get_task_status(self, task_id):
        for root in self.recursion_controller.tasks.values():
            if task_id in root:
                return root[task_id]
        return {}
