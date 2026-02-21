from __future__ import annotations
from datetime import datetime, timezone
from optimization_system.models.experiment import Experiment, ExperimentType, ExperimentVariant, SuccessCriterion
class ExperimentFramework:
    def __init__(self,experiment_runner,experiment_analyzer,experiment_store,config): self.runner=experiment_runner;self.analyzer=experiment_analyzer;self.store=experiment_store;self.config=config
    def create_experiment(self,name,hypothesis,control,treatment,metrics,sample_size=50,success_criteria=None):
        e=Experiment(name=name,description=name,experiment_type=ExperimentType.CAPABILITY_COMPARISON,hypothesis=hypothesis,control=control,treatment=treatment,metrics_to_compare=metrics,sample_size=sample_size,success_criteria=success_criteria or [SuccessCriterion(metrics[0],'lt',0,True)])
        self.store.save(e);return e
    def run_experiment(self,experiment):
        e=self.runner.run(experiment);e.status=e.status.ANALYZING;self.analyzer.analyze(e);e.status=e.status.COMPLETED;e.completed_at=datetime.now(timezone.utc);self.store.save(e);return e
    def create_capability_experiment(self,current_id,candidate_id,sample_size=50):
        return self.create_experiment('capability_ab',f'{candidate_id} better than {current_id}',ExperimentVariant('control',capability_id=current_id),ExperimentVariant('treatment',capability_id=candidate_id),['latency_ms','success'],sample_size)
    def create_strategy_experiment(self,current_name,candidate_name,goals,sample_size=20):
        e=Experiment(name='strategy_ab',description='strategy compare',experiment_type=ExperimentType.STRATEGY_COMPARISON,hypothesis='candidate better',control=ExperimentVariant('control',strategy_name=current_name),treatment=ExperimentVariant('treatment',strategy_name=candidate_name),metrics_to_compare=['planning_duration_ms','success'],sample_size=sample_size)
        self.store.save(e);return e
    def get_experiment(self,experiment_id): return self.store.load(experiment_id)
    def get_all_experiments(self): return self.store.load_all()
    def get_active_experiments(self): return self.store.load_by_status('RUNNING')+self.store.load_by_status('COLLECTING')
