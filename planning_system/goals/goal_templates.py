from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GoalTemplate:
    name: str
    action: str
    domain: str
    default_steps: list[str] = field(default_factory=list)


TEMPLATES: dict[str, GoalTemplate] = {
    "TRAIN_ML_MODEL": GoalTemplate("TRAIN_ML_MODEL", "train", "ml", ["collect_data", "preprocess", "train", "evaluate", "save_model"]),
    "BUILD_API": GoalTemplate("BUILD_API", "build", "web", ["design_api", "implement_endpoints", "add_middleware", "test", "deploy"]),
    "PROCESS_DATA": GoalTemplate("PROCESS_DATA", "process", "data", ["load_data", "clean_data", "transform_data", "validate_data", "save_data"]),
    "DEPLOY_SERVICE": GoalTemplate("DEPLOY_SERVICE", "deploy", "infrastructure", ["build_artifact", "configure_environment", "deploy", "verify", "monitor"]),
    "RUN_ANALYSIS": GoalTemplate("RUN_ANALYSIS", "analyze", "data", ["load_data", "analyze", "generate_report", "visualize"]),
    "AUTOMATE_TASK": GoalTemplate("AUTOMATE_TASK", "automate", "automation", ["define_trigger", "implement_action", "configure_schedule", "test", "activate"]),
    "SETUP_ENVIRONMENT": GoalTemplate("SETUP_ENVIRONMENT", "setup", "infrastructure", ["check_requirements", "install_dependencies", "configure", "validate"]),
}


def get_template(action: str, domain: str) -> GoalTemplate | None:
    for t in TEMPLATES.values():
        if t.action == action and t.domain == domain:
            return t
    return None


def match_template(goal) -> GoalTemplate | None:
    return get_template(goal.intent.action, goal.intent.domain)


def apply_template(goal, template: GoalTemplate):
    goal.metadata.setdefault("template_steps", template.default_steps)
    return goal


def list_templates() -> list[GoalTemplate]:
    return list(TEMPLATES.values())


def register_template(template: GoalTemplate) -> None:
    TEMPLATES[template.name] = template
