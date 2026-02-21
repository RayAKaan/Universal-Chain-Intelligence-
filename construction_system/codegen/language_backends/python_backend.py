from __future__ import annotations
import ast
from construction_system.codegen.language_backends.base_backend import BaseBackend
class PythonBackend(BaseBackend):
    language='python';file_extension='.py'
    def generate_file(self,spec,template_vars):return template_vars.get('code','')
    def validate_syntax(self,code):
        try: ast.parse(code);compile(code,'<generated>','exec');return True,[]
        except Exception as e:return False,[str(e)]
    def extract_imports(self,code):
        t=ast.parse(code);out=[]
        for n in ast.walk(t):
            if isinstance(n,ast.Import): out+=[a.name for a in n.names]
            if isinstance(n,ast.ImportFrom): out+=[n.module or '']
        return out
    def extract_functions(self,code):
        t=ast.parse(code);return [n.name for n in ast.walk(t) if isinstance(n,ast.FunctionDef)]
    def extract_classes(self,code):
        t=ast.parse(code);return [n.name for n in ast.walk(t) if isinstance(n,ast.ClassDef)]
    def check_imports_available(self,imports):
        import importlib
        r={}
        for i in imports:
            try:importlib.import_module(i.split('.')[0]);r[i]=True
            except Exception:r[i]=False
        return r
