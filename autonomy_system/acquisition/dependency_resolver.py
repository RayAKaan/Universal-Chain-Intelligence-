from __future__ import annotations
class DependencyResolver:
    def resolve(self,package_name): return []
    def check_conflicts(self,package_name): return []
    def get_dependency_tree(self,package_name): return {'name':package_name,'dependencies':[]}
