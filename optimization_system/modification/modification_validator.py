class ModificationValidator:
    def validate_pre_apply(self,modification): return (bool(modification.rollback_available), [] if modification.rollback_available else ['rollback missing'])
    def validate_post_apply(self,modification): return (modification.applied, [] if modification.applied else ['not applied'])
