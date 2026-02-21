from __future__ import annotations
def score_to_status(score:float)->str: return 'healthy' if score>=0.75 else 'degraded' if score>=0.5 else 'unhealthy'
