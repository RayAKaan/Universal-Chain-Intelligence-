from __future__ import annotations
import json
from dataclasses import asdict, is_dataclass
from datetime import datetime

def _default(o):
    if isinstance(o,datetime): return o.isoformat()
    if is_dataclass(o): return asdict(o)
    if hasattr(o,'value'): return o.value
    return str(o)

def serialize_specification(spec)->str:return json.dumps(spec.to_dict() if hasattr(spec,'to_dict') else asdict(spec),default=_default)
def deserialize_specification(data):
    from construction_system.models.specification import Specification
    return Specification.from_dict(json.loads(data))
def serialize_blueprint(b)->str:return json.dumps(asdict(b),default=_default)
def deserialize_blueprint(data):
    from construction_system.models.blueprint import Blueprint
    return Blueprint(**json.loads(data))
def serialize_artifact(a)->str:return json.dumps(asdict(a),default=_default)
def deserialize_artifact(data):
    from construction_system.models.artifact import Artifact
    return Artifact(**json.loads(data))
def serialize_build_result(r)->str:return json.dumps(asdict(r),default=_default)
def deserialize_build_result(data):
    from construction_system.models.build_result import BuildResult
    return BuildResult(**json.loads(data))
def serialize_provenance_record(r)->str:return json.dumps(asdict(r),default=_default)
def deserialize_provenance_record(data):
    from construction_system.models.provenance_record import ProvenanceRecord
    return ProvenanceRecord(**json.loads(data))
