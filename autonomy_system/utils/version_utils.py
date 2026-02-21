from __future__ import annotations
def parse_version(v:str): return tuple(int(x) for x in v.split('.') if x.isdigit())
