from __future__ import annotations
from dataclasses import dataclass, field
class ValidationError(Exception):pass
@dataclass
class ValidationIssue:severity:str;code_unit_id:str;line:int;message:str;suggestion:str=''
@dataclass
class ValidationReport:
    is_valid:bool;syntax_results:list=field(default_factory=list);analysis_results:list=field(default_factory=list);test_results:dict=field(default_factory=dict);overall_score:float=0.0;issues:list[ValidationIssue]=field(default_factory=list)
class CodeValidator:
    def __init__(self,syntax_checker,static_analyzer,test_runner,config=None):
        self.syntax_checker=syntax_checker;self.static_analyzer=static_analyzer;self.test_runner=test_runner;self.config=config
    def validate(self,code_units,blueprint):
        syntax=[];analysis=[];issues=[]
        for u in code_units:
            s=self.syntax_checker.check_all(u.code,u.language);syntax.append(s)
            for e in s.errors: issues.append(ValidationIssue('error',u.unit_id,1,e,''))
            a=self.static_analyzer.analyze(u.code);analysis+=a
            for x in a:
                sev=x.get('severity','info');issues.append(ValidationIssue(sev,u.unit_id,x.get('line',1),x.get('message',''),''))
        test={'total':0,'passed':0,'failed':0,'errors':0,'skipped':0,'duration_ms':0,'details':[]}
        valid=not any(i.severity=='error' for i in issues)
        score=max(0.0,1.0-len([i for i in issues if i.severity=='error'])*0.2-len([i for i in issues if i.severity=='warning'])*0.05)
        return ValidationReport(valid,syntax,analysis,test,score,issues)
