
from pathlib import Path
import mimetypes

class StaticHandler:
    def __init__(self, static_dir, template_dir):
        self.static_dir=Path(static_dir)
        self.template_dir=Path(template_dir)
    def resolve(self, path):
        if path in ('/','/index.html'): return self.template_dir/'index.html'
        if path.startswith('/static/'): return self.static_dir/path[len('/static/'):]
        return None
    def read(self, fp):
        return fp.read_bytes(), (mimetypes.guess_type(str(fp))[0] or 'application/octet-stream')
