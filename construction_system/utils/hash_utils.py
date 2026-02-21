from __future__ import annotations
import hashlib, json, uuid
from pathlib import Path

def hash_string(s:str)->str:return hashlib.sha256(s.encode()).hexdigest()
def hash_file(path:str)->str:return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def hash_dict(d:dict)->str:return hash_string(json.dumps(d,sort_keys=True,default=str))
def generate_id()->str:return str(uuid.uuid4())
def short_id()->str:return uuid.uuid4().hex[:8]
