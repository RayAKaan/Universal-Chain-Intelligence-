from __future__ import annotations
class TelemetryExporter:
    def export(self,points): return [p.__dict__ for p in points]
