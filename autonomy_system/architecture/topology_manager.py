from __future__ import annotations
class TopologyManager:
    def get_topology(self): return {'phases':['phase0','phase1','phase2','phase3','phase4'],'connections':[('phase2','phase1'),('phase2','phase0'),('phase4','phase3')]}
    def visualize_topology(self): return 'phase2 -> phase1 -> phase0\nphase4 -> phase3 -> phase1'
