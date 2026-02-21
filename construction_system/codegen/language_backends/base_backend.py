from __future__ import annotations
from abc import ABC, abstractmethod
class BaseBackend(ABC):
    language='';file_extension=''
    @abstractmethod
    def generate_file(self,spec,template_vars):...
    @abstractmethod
    def validate_syntax(self,code):...
    def get_comment_syntax(self):return '#','"""','"""'
