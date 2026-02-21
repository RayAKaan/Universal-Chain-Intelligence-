from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
class StatePersistence:
    def __init__(self,path='data/uci_state.json',checkpoint_dir='data/checkpoints'):
        self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True); self.cdir=Path(checkpoint_dir); self.cdir.mkdir(parents=True,exist_ok=True)
    def save_state(self,state): self.path.write_text(json.dumps(state,default=str))
    def load_state(self): return json.loads(self.path.read_text()) if self.path.exists() else {}
    def save_checkpoint(self,name=None):
        cid=name or datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
        p=self.cdir/f'{cid}.json'; p.write_text(json.dumps(self.load_state(),default=str)); return cid
    def restore_checkpoint(self,checkpoint_id):
        p=self.cdir/f'{checkpoint_id}.json'; return json.loads(p.read_text()) if p.exists() else {}
    def get_checkpoints(self): return [{'id':p.stem,'path':str(p)} for p in sorted(self.cdir.glob('*.json'))]
