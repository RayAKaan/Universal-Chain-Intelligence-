from __future__ import annotations

from construction_system.models.recursive_task import RecursiveTask


class SpecificationError(Exception):
    pass


class ConstructionManager:
    def __init__(self, spec_validator, spec_resolver, template_library, constructors, subtask_generator, recursive_engine, validator, sandbox_manager, artifact_manager, provenance_tracker, phase1_bridge, phase2_bridge, database, config, capability_registry=None):
        self.spec_validator = spec_validator
        self.spec_resolver = spec_resolver
        self.template_library = template_library
        self.constructors = constructors
        self.subtask_generator = subtask_generator
        self.recursive_engine = recursive_engine
        self.validator = validator
        self.sandbox_manager = sandbox_manager
        self.artifact_manager = artifact_manager
        self.provenance_tracker = provenance_tracker
        self.phase1_bridge = phase1_bridge
        self.phase2_bridge = phase2_bridge
        self.database = database
        self.config = config
        self.capability_registry = capability_registry

    def select_constructor(self, spec):
        for c in self.constructors:
            if c.can_construct(spec):
                return c
        return self.constructors[0]

    def construct_direct(self, spec, recursive_context):
        return self.select_constructor(spec).construct(spec, recursive_context)

    def construct(self, spec):
        valid, issues = self.spec_validator.validate(spec)
        if not valid:
            raise SpecificationError(issues)
        spec = self.spec_resolver.resolve_dependencies(spec, self.capability_registry)
        spec = self.spec_resolver.resolve_templates(spec, self.template_library)
        if self.subtask_generator.should_decompose(spec):
            task = RecursiveTask(specification=spec, name=spec.name, description=spec.description, root_task_id="", max_depth=self.config.MAX_RECURSION_DEPTH)
            task.root_task_id = task.task_id
            return self.recursive_engine.execute_recursive(task)

        result = self.construct_direct(spec, None)
        if self.config.VALIDATE_SYNTAX:
            self.validator.validate(result.code_units, result.blueprint)
        if self.config.RUN_TESTS and result.files_created:
            self.sandbox_manager.execute_file_in_sandbox(result.files_created[0])
        if spec.spec_type.value == "CAPABILITY_PLUGIN" and self.phase1_bridge:
            self.phase1_bridge.register_constructed_capability(None, spec)
        if spec.spec_type.value == "STRATEGY_PLUGIN" and self.phase2_bridge:
            self.phase2_bridge.register_constructed_strategy(None, spec)
        self.database.execute(
            "INSERT OR REPLACE INTO build_results(result_id,blueprint_id,spec_id,status,data,created_at) VALUES(?,?,?,?,?,datetime('now'))",
            (result.result_id, result.blueprint_id, result.spec_id, result.status.value, str(result.__dict__)),
        )
        return result
