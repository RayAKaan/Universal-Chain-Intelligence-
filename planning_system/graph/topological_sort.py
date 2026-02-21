from __future__ import annotations

from collections import defaultdict, deque


class CycleDetectedError(Exception):
    pass


def topological_sort(nodes: dict, edges: list) -> list[str]:
    indeg = {n: 0 for n in nodes}
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
        indeg[b] = indeg.get(b, 0) + 1
    q = deque([n for n, d in indeg.items() if d == 0])
    out = []
    while q:
        n = q.popleft()
        out.append(n)
        for m in adj.get(n, []):
            indeg[m] -= 1
            if indeg[m] == 0:
                q.append(m)
    if len(out) != len(nodes):
        raise CycleDetectedError("cycle detected")
    return out


def detect_cycle(nodes: dict, edges: list) -> list[str]:
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
    seen, stack = set(), set()
    path = []

    def dfs(n):
        seen.add(n)
        stack.add(n)
        path.append(n)
        for m in adj.get(n, []):
            if m not in seen and dfs(m):
                return True
            if m in stack:
                path.append(m)
                return True
        stack.remove(n)
        path.pop()
        return False

    for n in nodes:
        if n not in seen and dfs(n):
            return path
    return []


def all_topological_sorts(nodes: dict, edges: list) -> list[list[str]]:
    if len(nodes) > 8:
        return [topological_sort(nodes, edges)]
    adj = defaultdict(list)
    indeg = {n: 0 for n in nodes}
    for a, b in edges:
        adj[a].append(b)
        indeg[b] += 1
    out = []

    def backtrack(order, indeg_local):
        if len(out) >= 100:
            return
        zeroes = [n for n in nodes if indeg_local[n] == 0 and n not in order]
        if not zeroes:
            if len(order) == len(nodes):
                out.append(order.copy())
            return
        for z in zeroes:
            nxt = indeg_local.copy()
            for k in adj[z]:
                nxt[k] -= 1
            backtrack(order + [z], nxt)

    backtrack([], indeg)
    return out
