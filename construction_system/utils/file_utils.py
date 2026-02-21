from __future__ import annotations
import hashlib, shutil, tempfile
from pathlib import Path

def write_file(path:str,content:str)->None:
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding='utf-8')
def read_file(path:str)->str:return Path(path).read_text(encoding='utf-8')
def file_exists(path:str)->bool:return Path(path).exists()
def create_directory(path:str)->None:Path(path).mkdir(parents=True,exist_ok=True)
def delete_directory(path:str)->None:shutil.rmtree(path,ignore_errors=True)
def list_files(directory:str,extension:str=None)->list[str]:
    p=Path(directory)
    if not p.exists():return []
    items=[str(x) for x in p.rglob('*') if x.is_file()]
    return [i for i in items if (not extension or i.endswith(extension))]
def copy_file(src:str,dst:str)->None:
    Path(dst).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
def get_file_size(path:str)->int:return Path(path).stat().st_size
def get_file_checksum(path:str)->str:return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def create_temp_directory(prefix:str='uci_')->str:return tempfile.mkdtemp(prefix=prefix)
def cleanup_temp_directory(path:str)->None:shutil.rmtree(path,ignore_errors=True)
