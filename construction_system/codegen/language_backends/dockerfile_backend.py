from __future__ import annotations

from construction_system.codegen.language_backends.base_backend import BaseBackend


class DockerfileBackend(BaseBackend):
    language = "dockerfile"
    file_extension = ""

    def generate_file(self, spec, template_vars):
        return (
            f"FROM {template_vars.get('base_image', 'python:3.11-slim')}\n"
            "WORKDIR /app\n"
            "COPY . /app\n"
            f"ENTRYPOINT [\"python\", \"{template_vars.get('entrypoint', 'main.py')}\"]\n"
        )

    def validate_syntax(self, code):
        allowed = {"FROM", "WORKDIR", "COPY", "RUN", "CMD", "ENTRYPOINT", "ENV", "EXPOSE", "ARG", "LABEL"}
        valid = all(line.split(" ")[0] in allowed for line in code.splitlines() if line.strip())
        return valid, ([] if valid else ["invalid dockerfile instructions"])
