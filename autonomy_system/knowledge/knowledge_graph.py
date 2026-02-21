from __future__ import annotations
class KnowledgeGraph:
    def __init__(self): self.t=[]
    def add_triple(self,s,p,o): self.t.append((s,p,o))
    def remove_triple(self,s,p,o): self.t=[x for x in self.t if x!=(s,p,o)]
    def get_related(self,e): return [{'subject':s,'predicate':p,'object':o} for s,p,o in self.t if s==e or o==e]
    def get_connections(self,a,b): return [x for x in self.get_related(a) if x['object']==b or x['subject']==b]
    def get_all_subjects(self): return sorted(set(s for s,_,_ in self.t))
    def get_all_predicates(self): return sorted(set(p for _,p,_ in self.t))
    def visualize(self): return '\n'.join(f'{s} -[{p}]-> {o}' for s,p,o in self.t)
