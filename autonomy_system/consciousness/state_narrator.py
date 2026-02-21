from __future__ import annotations
class StateNarrator:
    def format_duration(self,seconds):
        if seconds<60:return f'{int(seconds)} seconds'
        if seconds<3600:return f'{int(seconds//60)} minutes'
        return f'{int(seconds//3600)} hours {int((seconds%3600)//60)} minutes'
    def narrate_system_state(self,status): return f"Health: {status.overall_status.value}, autonomy: {status.autonomy_level}, uptime: {self.format_duration(status.uptime_seconds)}"
    def narrate_goal_progress(self,goal): return f"Goal '{goal.raw_input}' is in state {goal.status.value}."
    def narrate_improvement(self,improvement): return f"Applied improvement: {improvement}"
    def narrate_healing(self,event): return f"Detected {event.failure_type.value}, recovery success={event.recovery_success}."
