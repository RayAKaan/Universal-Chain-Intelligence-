from __future__ import annotations
import subprocess, tempfile, time
from pathlib import Path

def capture_execution(command,cwd,timeout,env=None):
    start=time.time();p=subprocess.run(command,cwd=cwd,env=env,capture_output=True,text=True,timeout=timeout,check=False)
    return {'stdout':p.stdout,'stderr':p.stderr,'exit_code':p.returncode,'duration_ms':(time.time()-start)*1000}

def capture_python_execution(code,cwd,timeout):
    fp=Path(cwd)/'_run.py';fp.write_text(code)
    return capture_execution(['python',str(fp)],cwd,timeout)
