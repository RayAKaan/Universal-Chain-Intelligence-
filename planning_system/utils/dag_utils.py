from __future__ import annotations

from collections import defaultdict, deque


def validate_dag(nodes, edges):
    return len(get_longest_path(nodes, edges, {n: 1 for n in nodes})) > 0 if nodes else True


def find_roots(nodes, edges):
    indeg = {n: 0 for n in nodes}
    for _, b in edges:
        indeg[b] += 1
    return [n for n, d in indeg.items() if d == 0]


def find_leaves(nodes, edges):
    out = {n: 0 for n in nodes}
    for a, _ in edges:
        out[a] += 1
    return [n for n, d in out.items() if d == 0]


def get_all_paths(source, target, edges):
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
    paths = []
    def dfs(n, p):
        if n == target:
            paths.append(p + [n]); return
        for m in adj.get(n, []):
            if m not in p:
                dfs(m, p + [n])
    dfs(source, [])
    return paths


def get_longest_path(nodes, edges, weights):
    roots = find_roots(nodes, edges)
    leaves = find_leaves(nodes, edges)
    best = []
    for r in roots:
        for l in leaves:
            for p in get_all_paths(r, l, edges):
                if sum(weights.get(x, 1) for x in p) > sum(weights.get(x, 1) for x in best):
                    best = p
    return best


def get_shortest_path(nodes, edges, weights):
    roots = find_roots(nodes, edges)
    if not roots:
        return []
    src = roots[0]
    q = deque([(src, [src])])
    seen = {src}
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
    while q:
        n, p = q.popleft()
        if n in find_leaves(nodes, edges):
            return p
        for m in adj[n]:
            if m not in seen:
                seen.add(m)
                q.append((m, p + [m]))
    return []


def reverse_edges(edges):
    return [(b, a) for a, b in edges]


def transitive_reduction(edges):
    return list(dict.fromkeys(edges))
