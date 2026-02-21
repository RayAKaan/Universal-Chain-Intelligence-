from __future__ import annotations
import json
from pathlib import Path
from construction_system.models.specification import Specification
class SpecParser:
    def parse_dict(self,data): return Specification.from_dict(data)
    def parse_json(self,json_str): return self.parse_dict(json.loads(json_str))
    def parse_file(self,file_path): return self.parse_json(Path(file_path).read_text())
