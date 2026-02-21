VIOLATION_THRESHOLD_PROTOCOL = {"trigger": ">5 safety violations in 1 hour", "actions": ["activate panic mode", "alert human"]}
CONTAINMENT_BREACH_PROTOCOL = {"trigger": "containment boundary breached", "actions": ["block operation", "alert human", "increase monitoring"]}
ALIGNMENT_DRIFT_PROTOCOL = {"trigger": "alignment score below 0.6", "actions": ["reduce autonomy", "alert human", "run alignment check"]}
RESOURCE_EXHAUSTION_PROTOCOL = {"trigger": "resource near exhaustion", "actions": ["cancel non-essential operations", "free resources", "alert human"]}
CORRUPTION_PROTOCOL = {"trigger": "data corruption detected", "actions": ["halt affected operations", "attempt recovery", "alert human"]}
