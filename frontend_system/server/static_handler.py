
from pathlib import Path
import mimetypes

class StaticHandler:
    def __init__(self, static_dir: str, template_dir: str):
        self.static_dir = Path(static_dir)
        self.template_dir = Path(template_dir)

    def resolve(self, path: str):
        if path == '/' or path == '/index.html':
            return self.template_dir / 'index.html'
        if path.startswith('/static/'):
            return self.static_dir / path.replace('/static/','',1)
        return None

    def read(self, file_path: Path):
        data=file_path.read_bytes(); ctype=mimetypes.guess_type(str(file_path))[0] or 'application/octet-stream'
        return data, ctype
