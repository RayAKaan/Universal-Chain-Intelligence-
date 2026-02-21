from __future__ import annotations
from optimization_system.models.modification import Modification, ModificationType
class CapabilityUpgrader:
    def check_for_upgrades(self,capability_id): return {'capability_id':capability_id,'version':'2.0'}
    def upgrade(self,capability_id,new_version): return Modification(ModificationType.CAPABILITY_CONFIG_CHANGE,'Upgrade capability','upgrade','phase1','registry',capability_id,str(new_version),before_state={'version':'1.0'},after_state=new_version,rollback_data={'version':'1.0'})
    def batch_upgrade(self,upgrade_list): return [self.upgrade(u['capability_id'],u) for u in upgrade_list]
