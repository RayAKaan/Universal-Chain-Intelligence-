from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed

from planning_system.models.execution_result import ExecutionResult


class ExecutionCoordinator:
    def __init__(self, execution_graph, step_executor, config, monitor=None, failure_handler=None):
        self.graph = execution_graph
        self.step_executor = step_executor
        self.config = config
        self.monitor = monitor
        self.failure_handler = failure_handler

    def execute_level(self, nodes, context):
        results = []
        with ThreadPoolExecutor(max_workers=min(len(nodes), self.config.MAX_PARALLEL_STEPS)) as pool:
            fut = {pool.submit(self.step_executor.execute_with_timeout, n.step, context): n for n in nodes}
            for f in as_completed(fut):
                results.append((fut[f], f.result()))
        return results

    def handle_completion(self, node, result, context):
        self.graph.mark_completed(node.node_id)

    def handle_failure(self, node, error, context):
        return node.step.on_failure

    def run(self, context):
        out = ExecutionResult(plan_id=context.plan_id, goal_id=context.goal_id, status="success")
        levels = self.graph.get_execution_levels()
        for lvl in levels:
            pending = [n for n in lvl if all(self.graph.nodes[p].step.status == "COMPLETED" for p in n.incoming_edges)]
            if not pending:
                continue
            pairs = self.execute_level(pending, context)
            for node, res in pairs:
                out.step_results.append(res)
                if res.status == "COMPLETED":
                    node.step.status = "COMPLETED"
                    self.handle_completion(node, res, context)
                else:
                    node.step.status = "FAILED"
                    out.status = "partial_success"
        out.steps_completed = len([r for r in out.step_results if r.status == "COMPLETED"])
        out.steps_failed = len([r for r in out.step_results if r.status == "FAILED"])
        return out
