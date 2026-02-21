from __future__ import annotations

import json


class ConfigBackend:
    language = "config"
    file_extension = ".json"

    def generate_json(self, data):
        return json.dumps(data, indent=2, sort_keys=True)

    def generate_yaml(self, data):
        return self.generate_json(data)

    def generate_ini(self, data):
        lines = []
        for sec, vals in data.items():
            lines.append(f"[{sec}]")
            for k, v in vals.items():
                lines.append(f"{k}={v}")
        return "\n".join(lines) + "\n"

    def generate_env(self, data):
        return "\n".join(f"{k}={v}" for k, v in data.items()) + "\n"
