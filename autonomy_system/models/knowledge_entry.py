from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
class KnowledgeType(str,Enum): FACT='FACT'; RULE='RULE'; PREFERENCE='PREFERENCE'; PATTERN='PATTERN'; PROCEDURE='PROCEDURE'; RELATIONSHIP='RELATIONSHIP'; CONSTRAINT='CONSTRAINT'
@dataclass
class KnowledgeEntry:
    knowledge_type:KnowledgeType; subject:str; predicate:str; object:str; confidence:float; source:str
    entry_id:str=field(default_factory=lambda:str(uuid4())); context:dict=field(default_factory=dict); valid_from:datetime=field(default_factory=lambda:datetime.now(timezone.utc)); valid_until:datetime|None=None; access_count:int=0; last_accessed:datetime|None=None; created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc)); updated_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
