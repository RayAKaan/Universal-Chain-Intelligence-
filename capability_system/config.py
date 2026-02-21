from __future__ import annotations

DATABASE_PATH = "data/uci_capabilities.db"
PLUGIN_DIRECTORY = "plugins/"
MODEL_DIRECTORIES = ["models/", "~/.cache/huggingface/"]

DISCOVERY_INTERVAL_SECONDS = 300
HEALTH_CHECK_INTERVAL_SECONDS = 60
BENCHMARK_INTERVAL_HOURS = 24

BENCHMARK_DEFAULT_ITERATIONS = 100
BENCHMARK_WARMUP_ITERATIONS = 10
BENCHMARK_TIMEOUT_MS = 30000

HEALTH_CONSECUTIVE_FAILURES_DEGRADED = 3
HEALTH_CONSECUTIVE_FAILURES_FAILED = 10

SCANNER_TIMEOUT_SECONDS = 30
API_REQUEST_TIMEOUT_SECONDS = 10

KNOWN_TOOLS = {
    "ffmpeg": {"category": "media", "subcategory": "video_processing"},
    "curl": {"category": "network", "subcategory": "http_client"},
    "git": {"category": "development", "subcategory": "version_control"},
    "docker": {"category": "infrastructure", "subcategory": "containerization"},
    "python3": {"category": "runtime", "subcategory": "interpreter"},
    "node": {"category": "runtime", "subcategory": "interpreter"},
    "gcc": {"category": "development", "subcategory": "compiler"},
    "make": {"category": "development", "subcategory": "build_tool"},
    "pip": {"category": "development", "subcategory": "package_manager"},
    "npm": {"category": "development", "subcategory": "package_manager"},
}

API_ENDPOINTS = []

NETWORK_SCAN_ENABLED = False
NETWORK_SCAN_RANGE = "192.168.1.0/24"
NETWORK_SCAN_PORTS = [8000, 8080, 8888, 11434, 5000]

LOG_LEVEL = "INFO"
LOG_FILE = "logs/capability_system.log"

EXCLUDED_PYTHON_PACKAGES = [
    "pip", "setuptools", "wheel", "pkg_resources", "_distutils_hack", "__pycache__"
]
