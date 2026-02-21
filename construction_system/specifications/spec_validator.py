from __future__ import annotations
class SpecificationError(Exception):pass
class SpecValidator:
    def validate(self,spec):
        issues=[]
        if not spec.name: issues.append('name required')
        if not spec.spec_type: issues.append('spec_type required')
        ids={c.component_id for c in spec.components}
        for c in spec.components:
            for d in c.dependencies:
                if d not in ids: issues.append(f'missing component dependency {d}')
        # cycle check
        graph={c.component_id:set(c.dependencies) for c in spec.components}
        seen=set();stack=set()
        def dfs(n):
            seen.add(n);stack.add(n)
            for m in graph.get(n,set()):
                if m not in seen and dfs(m): return True
                if m in stack: return True
            stack.remove(n);return False
        for n in graph:
            if n not in seen and dfs(n): issues.append('circular component dependencies');break
        return len(issues)==0,issues
