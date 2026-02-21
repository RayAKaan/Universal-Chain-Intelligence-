from __future__ import annotations
class InterfaceMatcher:
    def check_compatibility(self,interface_a,interface_b):
        a={m.method_name for m in getattr(interface_a,'methods',[])};b={m.method_name for m in getattr(interface_b,'methods',[])}
        return len(a&b)/len(a|b) if (a|b) else 1.0
    def match_interfaces(self,provider,consumer):
        out=[]
        for pi in provider.provided_interfaces:
            for ci in consumer.required_interfaces:
                score=self.check_compatibility(pi,ci)
                out.append({'provider_interface':getattr(pi,'name',str(pi)),'provider_method':'*','consumer_interface':getattr(ci,'name',str(ci)),'consumer_method':'*','compatibility_score':score,'requires_adapter':score<1.0})
        return out
    def find_compatible_components(self,component,all_components):
        out=[]
        for c in all_components:
            if c.component_id==component.component_id: continue
            score=1.0 if c.component_type==component.component_type else 0.5
            out.append((c,score))
        return sorted(out,key=lambda x:x[1],reverse=True)
