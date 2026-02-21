class ResourceAnalyzer:
    def analyze_utilization(self): return {'cpu':70,'memory':65,'disk':40,'threads':60,'queue_capacity':30,'overutilized':['cpu']}
    def analyze_waste(self): return {'idle_memory_mb':256,'unused_threads':2,'over_provisioned_capabilities':['legacy_tool']}
    def analyze_contention(self): return [{'resource':'cpu','component':'heavy_model','severity':'medium'}]
