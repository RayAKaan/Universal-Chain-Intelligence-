from __future__ import annotations

import re

ACTIONS = [
    "build","create","make","deploy","analyze","transform","optimize","fix","monitor","automate","run","execute","generate","train","test","evaluate","install","configure","setup","process","convert","extract","scrape","download","upload","send","receive","schedule","clean","validate","migrate","backup","restore","search","find","query","calculate","compute","visualize","plot","render","compile","package","publish","serve","start","stop","restart",
]
DOMAINS = ["ml","web","data","infrastructure","automation","media","security","development","system","network","database","api","devops","testing","documentation"]
QUALIFIERS = ["fast","slow","accurate","lightweight","scalable","secure","distributed","real-time","batch","parallel","sequential","simple","complex","production","prototype","minimal"]


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_\-]+", text.lower())


def parse_action(text: str) -> str:
    toks = tokenize(text)
    for tok in toks:
        if tok in ACTIONS:
            return tok
    return "build"


def parse_target(text: str, action: str) -> str:
    t = text.lower()
    m = re.search(rf"{action}\s+(an?|the)?\s*([a-z0-9_\- ]+)", t)
    if m:
        return m.group(2).strip()
    return text.strip()


def parse_domain(text: str) -> str:
    t = text.lower()
    for d in DOMAINS:
        if d in t:
            return d
    if any(k in t for k in ["model", "classification", "training"]):
        return "ml"
    if "api" in t or "service" in t:
        return "web"
    if "data" in t or "csv" in t or "json" in t:
        return "data"
    return "system"


def parse_qualifiers(text: str) -> list[str]:
    t = tokenize(text)
    return [q for q in QUALIFIERS if q in t]


def parse_inputs(text: str) -> list[dict]:
    out = []
    for p in re.findall(r"([a-zA-Z0-9_\-/]+\.(csv|json|txt|png|jpg))", text.lower()):
        out.append({"name": p[0], "type": p[1], "description": "detected file", "required": True, "value": None, "source": "user"})
    return out


def parse_outputs(text: str) -> list[dict]:
    t = text.lower()
    out = []
    if "report" in t:
        out.append({"name": "report", "type": "document", "description": "analysis report", "success_criteria": "report generated"})
    if "model" in t:
        out.append({"name": "model", "type": "artifact", "description": "trained model", "success_criteria": "model saved"})
    if not out:
        out.append({"name": "result", "type": "generic", "description": "goal result", "success_criteria": "task completed"})
    return out


def parse_constraints(text: str) -> list[dict]:
    t = text.lower()
    out = []
    m = re.search(r"within\s+(\d+)\s+(minute|minutes|hour|hours|second|seconds)", t)
    if m:
        out.append({"constraint_type": "time", "parameter": "duration", "operator": "lte", "value": int(m.group(1)), "unit": m.group(2), "is_hard": True})
    if "minimal resources" in t or "under" in t and "ram" in t:
        out.append({"constraint_type": "resource", "parameter": "memory", "operator": "lte", "value": 1024, "unit": "mb", "is_hard": False})
    return out
