from __future__ import annotations
import importlib, importlib.util, sys

def safe_import(module_name:str):
    try:return importlib.import_module(module_name),True
    except Exception:return None,False
def check_import_available(module_name:str)->bool:return safe_import(module_name)[1]
def load_module_from_file(file_path:str,module_name:str):
    spec=importlib.util.spec_from_file_location(module_name,file_path)
    m=importlib.util.module_from_spec(spec);sys.modules[module_name]=m;spec.loader.exec_module(m);return m
def load_class_from_file(file_path:str,class_name:str):return getattr(load_module_from_file(file_path,'dyn_'+class_name),class_name)
def reload_module(module_name:str):return importlib.reload(importlib.import_module(module_name))
def get_module_path(module_name:str)->str:return importlib.import_module(module_name).__file__
