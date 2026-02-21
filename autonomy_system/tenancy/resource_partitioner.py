from __future__ import annotations
class ResourcePartitioner:
    def partition(self,tenant_id,total_resources): return {'tenant_id':tenant_id,'cpu_percent':min(50,total_resources.get('cpu_percent',100)/2)}
