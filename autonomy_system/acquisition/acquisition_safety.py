from __future__ import annotations
class AcquisitionSafety:
    BLOCKED_PACKAGES=['os-sys','python-dateutil-2']
    def __init__(self,config): self.config=config
    def check_safe(self,package_name,source):
        issues=[]
        if package_name in self.BLOCKED_PACKAGES or package_name in getattr(self.config,'BLOCKED_PACKAGES',[]): issues.append('blocked package')
        if source not in getattr(self.config,'TRUSTED_SOURCES',['pypi']): issues.append('untrusted source')
        return (not issues,issues)
