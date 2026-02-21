from __future__ import annotations
import ast, importlib
from dataclasses import dataclass, field
@dataclass
class SyntaxResult:valid:bool;errors:list[str]=field(default_factory=list);warnings:list[str]=field(default_factory=list)
class SyntaxChecker:
    def check_python_syntax(self,code):
        try:ast.parse(code);compile(code,'<c>','exec');return True,[]
        except Exception as e:return False,[str(e)]
    def check_imports(self,code):
        try:t=ast.parse(code)
        except Exception as e:return False,[str(e)]
        errs=[]
        for n in ast.walk(t):
            if isinstance(n,ast.Import):
                for a in n.names:
                    try:importlib.import_module(a.name.split('.')[0])
                    except Exception:errs.append(f'missing import {a.name}')
            if isinstance(n,ast.ImportFrom) and n.module:
                try:importlib.import_module(n.module.split('.')[0])
                except Exception:errs.append(f'missing import {n.module}')
        return len(errs)==0,errs
    def check_indentation(self,code):
        errs=[]
        for i,l in enumerate(code.splitlines(),1):
            if l.startswith(' ') and (len(l)-len(l.lstrip(' ')))%4!=0: errs.append(f'line {i}: indentation not multiple of 4')
        return len(errs)==0,errs
    def check_all(self,code,language='python'):
        e=[];w=[]
        if language=='python':
            for f in [self.check_python_syntax,self.check_imports,self.check_indentation]:
                ok,errs=f(code);e.extend(errs)
        return SyntaxResult(len(e)==0,e,w)
