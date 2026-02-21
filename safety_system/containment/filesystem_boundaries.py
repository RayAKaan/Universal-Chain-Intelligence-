from pathlib import Path

from safety_system.scope.boundary_definitions import ALLOWED_FILESYSTEM_PATHS, FORBIDDEN_FILESYSTEM_PATHS


class FilesystemBoundaries:
    def is_allowed(self, path: str, operation: str) -> bool:
        p = str(Path(path).resolve())
        if any(x.replace("~", str(Path.home())) in p for x in FORBIDDEN_FILESYSTEM_PATHS):
            return False
        return any(str(Path(a).resolve()) in p or path.startswith("./") for a in ALLOWED_FILESYSTEM_PATHS)
