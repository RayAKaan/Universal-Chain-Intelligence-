from __future__ import annotations

from collections import defaultdict

from capability_system.models.capability import Capability


class CapabilityIndex:
    def __init__(self) -> None:
        self.by_id: dict[str, Capability] = {}
        self.by_name: dict[str, list[Capability]] = defaultdict(list)
        self.by_type: dict[str, list[Capability]] = defaultdict(list)
        self.by_category: dict[str, list[Capability]] = defaultdict(list)
        self.by_tag: dict[str, list[Capability]] = defaultdict(list)
        self.by_state: dict[str, list[Capability]] = defaultdict(list)

    def rebuild_from(self, capabilities: list[Capability]) -> None:
        self.by_id.clear(); self.by_name.clear(); self.by_type.clear(); self.by_category.clear(); self.by_tag.clear(); self.by_state.clear()
        for c in capabilities:
            self.add(c)

    def add(self, capability: Capability) -> None:
        self.by_id[capability.capability_id] = capability
        self.by_name[capability.name].append(capability)
        self.by_type[capability.capability_type.value].append(capability)
        self.by_category[capability.category].append(capability)
        self.by_state[capability.state.value].append(capability)
        for tag in capability.metadata.get("tags", []):
            self.by_tag[tag].append(capability)

    def remove(self, capability_id: str) -> None:
        cap = self.by_id.pop(capability_id, None)
        if not cap:
            return
        self.rebuild_from(list(self.by_id.values()))

    def update(self, capability: Capability) -> None:
        self.remove(capability.capability_id)
        self.add(capability)

    def search(self, filters: dict) -> list[Capability]:
        caps = list(self.by_id.values())
        for k, v in filters.items():
            if k == "name":
                caps = [c for c in caps if c.name == v]
            elif k == "type":
                caps = [c for c in caps if c.capability_type.value == v]
            elif k == "category":
                caps = [c for c in caps if c.category == v]
            elif k == "state":
                caps = [c for c in caps if c.state.value == v]
            elif k == "is_enabled":
                caps = [c for c in caps if c.is_enabled == v]
        return caps
