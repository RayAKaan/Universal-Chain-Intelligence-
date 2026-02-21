from __future__ import annotations

import os
import re
from urllib.parse import urlparse

SEMVER_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[\w.-]+)?(?:\+[\w.-]+)?$")
IMPORT_PATH_PATTERN = re.compile(r"^[a-zA-Z_][\w]*(\.[a-zA-Z_][\w]*)+$")


def validate_semver(version: str) -> bool:
    return bool(SEMVER_PATTERN.match(version))


def validate_json_schema(schema: dict) -> bool:
    return isinstance(schema, dict)


def validate_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate_file_path(path: str) -> bool:
    return os.path.exists(path)


def validate_import_path(path: str) -> bool:
    return bool(IMPORT_PATH_PATTERN.match(path))
