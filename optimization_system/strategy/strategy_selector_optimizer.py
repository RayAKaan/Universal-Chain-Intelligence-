class StrategySelectorOptimizer:
    def __init__(self,evaluator): self.evaluator=evaluator
    def build_selection_table(self):
        rec=self.evaluator.get_strategy_recommendations('general','default')
        return {'general':{'default':rec[0][0] if rec else 'sequential'}}
    def optimize_selection_logic(self): return {'selection_table':self.build_selection_table(),'updated':True}
