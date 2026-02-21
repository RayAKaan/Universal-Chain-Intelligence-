from __future__ import annotations
class Phase0ConstructorBridge:
    def __init__(self,execution_engine,scheduler):self.engine=execution_engine;self.scheduler=scheduler
    def _exec(self,fn,*a,**k): return fn(*a,**k)
    def execute_code_generation(self,task): return self._exec(task['callable'],*task.get('args',[]),**task.get('kwargs',{}))
    def execute_validation(self,task): return self.execute_code_generation(task)
    def execute_sandbox(self,task): return self.execute_code_generation(task)
    def execute_file_operation(self,task): return self.execute_code_generation(task)
