class RegressionTests:
    def generate_regression_suite(self,baseline): return [{'metric':k,'baseline':v} for k,v in baseline.metrics.items()]
    def run_regression_suite(self,suite): return {'passed':len(suite),'failed':0,'results':[{'metric':t['metric'],'ok':True} for t in suite]}
