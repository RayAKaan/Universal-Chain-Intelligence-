from __future__ import annotations
class CapabilityFetcher:
    def search_pypi(self,query): return [{'name':query,'version':'latest','description':'mock result','downloads':0}]
    def search_local(self,query): return []
    def fetch_package_info(self,name): return {'name':name,'version':'latest','description':'mock'}
    def evaluate_package(self,name): return {'name':name,'recent_updates':True,'documentation':True,'license':'unknown'}
