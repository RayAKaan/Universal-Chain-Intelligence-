from __future__ import annotations

import re


class TemplateError(Exception):
    pass


class TemplateEngine:
    def extract_variables(self, s):
        return list(dict.fromkeys(re.findall(r"{{\s*([a-zA-Z0-9_\.]+)(?:\|[^}]*)?\s*}}", s)))

    def validate_template(self, s):
        errs = []
        if s.count("{% if") != s.count("{% endif %}"):
            errs.append("unbalanced if blocks")
        if s.count("{% for") != s.count("{% endfor %}"):
            errs.append("unbalanced for blocks")
        return (len(errs) == 0, errs)

    def _apply_filter(self, val, flt):
        if flt == "upper":
            return str(val).upper()
        if flt.startswith("indent:"):
            n = int(flt.split(":", 1)[1])
            return "\n".join(" " * n + line for line in str(val).splitlines())
        return val

    def render(self, template_string, variables):
        s = template_string
        loop_pat = re.compile(r"{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%}(.*?){%\s*endfor\s*%}", re.S)
        while True:
            m = loop_pat.search(s)
            if not m:
                break
            item, arr, body = m.groups()
            items = variables.get(arr, [])
            buf = []
            for it in items:
                local = dict(variables)
                local[item] = it
                buf.append(self.render(body, local))
            s = s[: m.start()] + "".join(buf) + s[m.end() :]
        if_pat = re.compile(r"{%\s*if\s+(\w+)\s*%}(.*?){%\s*endif\s*%}", re.S)
        while True:
            m = if_pat.search(s)
            if not m:
                break
            key, body = m.groups()
            s = s[: m.start()] + (self.render(body, variables) if variables.get(key) else "") + s[m.end() :]

        def repl(m):
            expr = m.group(1).strip()
            parts = [x.strip() for x in expr.split("|")]
            name = parts[0]
            val = variables.get(name, "")
            for f in parts[1:]:
                val = self._apply_filter(val, f)
            return str(val)

        return re.sub(r"{{\s*([^}]+)\s*}}", repl, s)
