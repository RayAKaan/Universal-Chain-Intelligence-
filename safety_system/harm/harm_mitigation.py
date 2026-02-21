from safety_system.models.harm_assessment import HarmItem


class HarmMitigation:
    def mitigate(self, harm: HarmItem) -> list[str]:
        base = ["use dry-run", "apply in sandbox", "add confirmation", "reduce scope"]
        if harm.category == "data_loss":
            base.insert(0, "create backup before action")
        return base
