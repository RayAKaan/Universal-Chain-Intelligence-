from __future__ import annotations
class DashboardData:
    def __init__(self,core): self.core=core
    def get_overview(self): s=self.core.get_status(); return {'uptime':s.uptime_seconds,'health':s.overall_score,'active_goals':len(self.core.goal_manager.get_active_goals()),'capability_count':len(self.core.get_capabilities()),'autonomy':s.autonomy_level}
    def get_phase_dashboard(self,phase): return {'phase':phase,'status':'healthy'}
    def get_goal_dashboard(self): return self.core.goal_manager.get_queue_status()
    def get_capability_dashboard(self): return {'count':len(self.core.get_capabilities())}
    def get_improvement_dashboard(self): return {'improvements':0}
    def get_resource_dashboard(self): return {'cpu':20,'memory':30}
