from __future__ import annotations
from abc import ABC, abstractmethod
class BaseAdapter(ABC):
    name='base'; protocol='base'
    def __init__(self,hub=None): self.hub=hub; self.running=False
    @abstractmethod
    def start(self): ...
    @abstractmethod
    def stop(self): ...
    def is_running(self): return self.running
    @abstractmethod
    def send(self,message): ...
    @abstractmethod
    def receive(self): ...
