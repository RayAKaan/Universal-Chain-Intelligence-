from __future__ import annotations
from pathlib import Path
import os, signal
def write_pid(pid_file='uci.pid'): Path(pid_file).write_text(str(os.getpid()))
def read_pid(pid_file='uci.pid'): return int(Path(pid_file).read_text()) if Path(pid_file).exists() else 0
def remove_pid(pid_file='uci.pid'): Path(pid_file).unlink(missing_ok=True)
def is_running(pid_file='uci.pid'):
    pid=read_pid(pid_file)
    if not pid:return False
    try: os.kill(pid,0); return True
    except Exception: return False
