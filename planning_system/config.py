from __future__ import annotations

DATABASE_PATH = "data/uci_planning.db"
DEFAULT_STRATEGY = "adaptive"
MAX_DECOMPOSITION_DEPTH = 10
MAX_PLAN_STEPS = 1000
MAX_PARALLEL_STEPS = 10
DEFAULT_STEP_TIMEOUT_MS = 60000
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY_MS = 1000
DEFAULT_BACKOFF_MULTIPLIER = 2.0
OPTIMIZATION_OBJECTIVES = ["minimize_duration", "maximize_reliability"]
COST_CPU_PER_CORE_HOUR = 0.01
COST_MEMORY_PER_GB_HOUR = 0.005
COST_GPU_PER_HOUR = 0.50
COST_API_CALL = 0.001
MAX_PLAN_DURATION_MS = 3600000
MAX_PEAK_CPU_CORES = 8
MAX_PEAK_MEMORY_MB = 16384
MAX_PEAK_GPU_COUNT = 2
PROGRESS_UPDATE_INTERVAL_MS = 5000
STALL_DETECTION_TIMEOUT_MS = 300000
MAX_PLANNING_MEMORY_ENTRIES = 10000
SIMILAR_GOAL_THRESHOLD = 0.6
LOG_LEVEL = "INFO"
LOG_FILE = "logs/planning_system.log"
DECOMPOSITION_KNOWLEDGE = {
    "train_model": {"steps": ["collect_data", "preprocess_data", "configure_model", "train", "evaluate", "save_model"], "domain": "ml"},
    "deploy_service": {"steps": ["build", "test", "containerize", "push", "deploy", "verify", "monitor"], "domain": "infrastructure"},
    "process_data": {"steps": ["load_data", "validate_data", "clean_data", "transform_data", "save_data"], "domain": "data"},
    "build_api": {"steps": ["design_api", "implement_routes", "add_middleware", "implement_auth", "test", "document", "deploy"], "domain": "web"},
    "analyze_data": {"steps": ["load_data", "explore_data", "statistical_analysis", "generate_insights", "create_visualizations", "generate_report"], "domain": "data"},
    "setup_environment": {"steps": ["check_system", "install_dependencies", "configure_settings", "validate_setup"], "domain": "infrastructure"},
    "run_pipeline": {"steps": ["load_input", "stage_1_process", "stage_2_process", "stage_3_process", "collect_output"], "domain": "automation"},
    "build_web_app": {"steps": ["setup_project", "implement_backend", "implement_frontend", "implement_database", "integrate_components", "test", "deploy"], "domain": "web"},
    "create_report": {"steps": ["gather_data", "analyze_data", "create_charts", "write_narrative", "format_report", "export"], "domain": "data"},
    "optimize_system": {"steps": ["profile_system", "identify_bottlenecks", "implement_optimizations", "benchmark", "validate_improvements"], "domain": "system"},
}
