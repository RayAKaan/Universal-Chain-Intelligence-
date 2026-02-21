from __future__ import annotations
import ast
class StaticAnalyzer:
    def analyze(self,code):
        r=[]
        try:t=ast.parse(code)
        except Exception as e:return [{'rule':'parse','severity':'error','line':1,'message':str(e)}]
        for n in ast.walk(t):
            if isinstance(n,ast.ExceptHandler) and n.type is None:r.append({'rule':'bare_except','severity':'warning','line':n.lineno,'message':'bare except'})
            if isinstance(n,ast.FunctionDef):
                if len(n.args.args)>7:r.append({'rule':'too_many_parameters','severity':'warning','line':n.lineno,'message':'too many parameters'})
                if not ast.get_docstring(n):r.append({'rule':'missing_docstring','severity':'info','line':n.lineno,'message':'missing docstring'})
                if n.name.lower()!=n.name:r.append({'rule':'snake_case','severity':'info','line':n.lineno,'message':'function name not snake_case'})
            if isinstance(n,ast.ClassDef) and n.name[:1].islower():r.append({'rule':'pascal_case','severity':'info','line':n.lineno,'message':'class name should be PascalCase'})
        return r
