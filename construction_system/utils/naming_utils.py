from __future__ import annotations
import re

def sanitize_name(name:str)->str:return re.sub(r'[^a-zA-Z0-9_]+','_',name).strip('_')
def to_snake_case(name:str)->str:return sanitize_name(re.sub(r'([a-z0-9])([A-Z])',r'\1_\2',name).lower())
def to_pascal_case(name:str)->str:return ''.join(x.capitalize() for x in re.split(r'[_\-\s]+',sanitize_name(name)))
def to_camel_case(name:str)->str:
    p=to_pascal_case(name);return p[:1].lower()+p[1:] if p else p
def to_kebab_case(name:str)->str:return to_snake_case(name).replace('_','-')
def to_upper_snake_case(name:str)->str:return to_snake_case(name).upper()
def generate_module_name(spec_name:str)->str:return to_snake_case(spec_name)
def generate_class_name(spec_name:str)->str:return to_pascal_case(spec_name)
def generate_function_name(spec_name:str)->str:return to_snake_case(spec_name)
def is_valid_python_identifier(name:str)->bool:return name.isidentifier()
