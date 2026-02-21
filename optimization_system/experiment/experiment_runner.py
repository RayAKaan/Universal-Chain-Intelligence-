from __future__ import annotations
import random
from datetime import datetime, timezone
class ExperimentRunner:
    def __init__(self,phase1_bridge=None,phase2_bridge=None): self.p1=phase1_bridge;self.p2=phase2_bridge
    def generate_test_inputs(self,capability_id,count): return [{'input':i} for i in range(count)]
    def run_capability_sample(self,capability_id,test_input):
        perf=self.p1.get_capability_performance(capability_id) if self.p1 else {'latency_ms':100,'reliability':0.9}
        latency=max(1.0,random.gauss(perf.get('latency_ms',100),max(1.0,perf.get('latency_ms',100)*0.05)))
        success=random.random()<perf.get('reliability',0.9)
        return {'latency_ms':latency,'success':1.0 if success else 0.0,'resource_usage':random.uniform(0.1,0.9)}
    def run_strategy_sample(self,strategy_name,goal): return {'planning_duration_ms':random.uniform(100,400),'success':1.0,'plan_complexity':random.randint(3,12)}
    def run(self,experiment):
        experiment.status=experiment.status.RUNNING;experiment.started_at=datetime.now(timezone.utc)
        if experiment.experiment_type.value=='CAPABILITY_COMPARISON':
            for x in self.generate_test_inputs(experiment.control.capability_id,experiment.sample_size):
                experiment.control_results.append(self.run_capability_sample(experiment.control.capability_id,x))
                experiment.treatment_results.append(self.run_capability_sample(experiment.treatment.capability_id,x));experiment.current_samples+=1
        else:
            for i in range(experiment.sample_size):
                experiment.control_results.append(self.run_strategy_sample(experiment.control.strategy_name,f'g{i}'))
                experiment.treatment_results.append(self.run_strategy_sample(experiment.treatment.strategy_name,f'g{i}'));experiment.current_samples+=1
        experiment.status=experiment.status.COLLECTING
        return experiment
