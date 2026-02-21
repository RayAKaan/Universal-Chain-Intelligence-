class CapabilityRecommender:
    def recommend_new_capabilities(self): return [{'description':'Add cache capability','priority':'medium','source':'gaps'}]
    def recommend_upgrades(self): return [{'capability_id':'legacy_tool','version':'2.0'}]
