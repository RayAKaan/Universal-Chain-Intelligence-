from __future__ import annotations
from pathlib import Path
import json, threading, time
from autonomy_system.communication.protocol_adapters.base_adapter import BaseAdapter
class FileAdapter(BaseAdapter):
    name='file'; protocol='file'
    def __init__(self,hub=None,input_dir='goals',output_dir='results'): super().__init__(hub); self.inp=Path(input_dir); self.out=Path(output_dir); self.thread=None
    def _loop(self):
        self.inp.mkdir(parents=True,exist_ok=True); self.out.mkdir(parents=True,exist_ok=True)
        while self.running:
            for f in self.inp.glob('*.goal'):
                text=f.read_text(); msg={'message_id':f.stem,'text':text};
                if self.hub: resp=self.hub.handle_message(self.hub.parser.parse(text,'file')); self.out.joinpath(f'{f.stem}.result').write_text(json.dumps(resp.content,default=str))
                f.unlink(missing_ok=True)
            time.sleep(0.2)
    def start(self): self.running=True; self.thread=threading.Thread(target=self._loop,daemon=True); self.thread.start()
    def stop(self): self.running=False
    def send(self,message): pass
    def receive(self): return None
