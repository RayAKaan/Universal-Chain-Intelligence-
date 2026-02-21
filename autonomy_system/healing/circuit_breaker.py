from __future__ import annotations
import time
class CircuitBreakerOpenError(Exception): pass
class CircuitBreaker:
    def __init__(self,failure_threshold=5,recovery_timeout_seconds=60): self.failure_threshold=failure_threshold; self.recovery_timeout_seconds=recovery_timeout_seconds; self.state='CLOSED'; self.failures=0; self.last_failure=0.0
    def call(self,func,*args,**kwargs):
        if self.state=='OPEN' and time.time()-self.last_failure<self.recovery_timeout_seconds: raise CircuitBreakerOpenError('breaker open')
        if self.state=='OPEN': self.state='HALF_OPEN'
        try:
            out=func(*args,**kwargs); self.failures=0; self.state='CLOSED'; return out
        except Exception:
            self.failures+=1; self.last_failure=time.time();
            if self.failures>=self.failure_threshold: self.state='OPEN'
            raise
    def get_state(self): return self.state
    def reset(self): self.state='CLOSED'; self.failures=0
    def trip(self): self.state='OPEN'; self.last_failure=time.time()
class CircuitBreakerRegistry:
    def __init__(self): self.b={}
    def get_breaker(self,name): self.b.setdefault(name,CircuitBreaker()); return self.b[name]
    def get_all_breakers(self): return self.b
    def get_open_breakers(self): return [k for k,v in self.b.items() if v.get_state()=='OPEN']
