from __future__ import annotations
import importlib.util
class PackageInstaller:
    def install_python_package(self,name,version=None): return True
    def install_system_package(self,name): return False
    def uninstall_python_package(self,name): return True
    def is_installed(self,name): return importlib.util.find_spec(name) is not None
    def get_installed_version(self,name):
        try:
            import importlib.metadata as md
            return md.version(name)
        except Exception: return ''
