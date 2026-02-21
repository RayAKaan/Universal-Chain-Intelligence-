from safety_system.models.emergency_event import EmergencyEvent


class EmergencySystem:
    def __init__(self, config):
        from safety_system.emergency.kill_switch import KillSwitch
        from safety_system.emergency.panic_mode import PanicMode
        from safety_system.emergency.dead_man_switch import DeadManSwitch

        self.kill_switch = KillSwitch()
        self.panic_mode = PanicMode()
        self.dead_man_switch = DeadManSwitch()
        self.events = []

    def activate_kill_switch(self) -> None:
        self.kill_switch.activate("human")
        self.events.append(EmergencyEvent("kill_switch", "emergency", ["stop goals", "cancel active", "offline"], {}, {"state": "OFFLINE"}))

    def activate_panic_mode(self) -> None:
        self.panic_mode.activate("violation threshold")
        self.events.append(EmergencyEvent("panic_mode", "critical", ["stop new goals", "reduce autonomy"], {}, {"panic": True}))

    def deactivate_panic_mode(self, authorization: str) -> None:
        self.panic_mode.deactivate(authorization)

    def is_emergency_active(self) -> bool:
        return self.kill_switch.is_activated() or self.panic_mode.active

    def get_emergency_state(self) -> dict:
        return {"kill_switch": self.kill_switch.is_activated(), "panic_mode": self.panic_mode.active}
