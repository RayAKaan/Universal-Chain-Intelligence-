from __future__ import annotations

from pathlib import Path

from construction_system.models.artifact import Artifact
from construction_system.utils.file_utils import get_file_checksum, get_file_size, read_file


class ArtifactError(Exception):
    pass


class ArtifactManager:
    def __init__(self, artifact_store, provenance_tracker, config):
        self.store = artifact_store
        self.provenance = provenance_tracker
        self.config = config

    def register_artifact(self, name, file_path, artifact_type, source_spec_id, source_blueprint_id, metadata=None):
        p = Path(file_path)
        a = Artifact(
            name=name,
            artifact_type=artifact_type,
            file_path=str(p),
            file_size_bytes=get_file_size(str(p)) if p.exists() else 0,
            checksum=get_file_checksum(str(p)) if p.exists() else "",
            source_spec_id=source_spec_id,
            source_blueprint_id=source_blueprint_id,
            metadata=metadata or {},
        )
        self.store.save(a)
        return a

    def get_artifact(self, artifact_id):
        return self.store.load(artifact_id)

    def get_artifacts_by_spec(self, spec_id):
        return self.store.search({"source_spec_id": spec_id})

    def get_artifacts_by_type(self, artifact_type):
        return self.store.search({"artifact_type": artifact_type})

    def get_all_artifacts(self):
        return self.store.load_all()

    def delete_artifact(self, artifact_id, delete_file=False):
        a = self.get_artifact(artifact_id)
        if not a:
            return False
        if delete_file and Path(a.file_path).exists():
            Path(a.file_path).unlink()
        self.store.delete(artifact_id)
        return True

    def verify_artifact(self, artifact_id):
        a = self.get_artifact(artifact_id)
        return bool(a and Path(a.file_path).exists() and get_file_checksum(a.file_path) == a.checksum)

    def get_artifact_content(self, artifact_id):
        a = self.get_artifact(artifact_id)
        return read_file(a.file_path) if a else ""

    def get_stats(self):
        all_a = self.get_all_artifacts()
        if not all_a:
            return {"total": 0, "by_type": {}, "total_size_bytes": 0}

        def type_name(a):
            t = getattr(a, "artifact_type", "unknown")
            return t.value if hasattr(t, "value") else str(t)

        by_type = {}
        for a in all_a:
            t = type_name(a)
            by_type[t] = by_type.get(t, 0) + 1
        return {
            "total": len(all_a),
            "by_type": by_type,
            "total_size_bytes": sum(getattr(a, "file_size_bytes", 0) for a in all_a),
        }
