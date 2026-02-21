from __future__ import annotations
class SourceRegistry:
    def __init__(self): self.sources=[{'name':'pypi','type':'pypi','url':'https://pypi.org','enabled':True,'priority':1},{'name':'local','type':'local','url':'file://','enabled':True,'priority':2}]
    def register_source(self,source): self.sources.append(source)
    def get_sources(self): return sorted(self.sources,key=lambda s:s.get('priority',99))
    def get_source(self,name): return next((s for s in self.sources if s['name']==name),None)
    def enable_source(self,name): s=self.get_source(name); s and s.update({'enabled':True})
    def disable_source(self,name): s=self.get_source(name); s and s.update({'enabled':False})
