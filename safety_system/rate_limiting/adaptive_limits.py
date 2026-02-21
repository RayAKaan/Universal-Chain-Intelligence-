class AdaptiveLimits:
    def adjust(self, base: int, pressure: float) -> int:
        if pressure > 0.8:
            return max(1, int(base * 0.5))
        return base
