def dfs(graph, start):
    visited = set()
    seen = {start}
    stack = [start]

    while stack:
        yield {
            "algo": "DFS",
            "action": "stack",
            "stack": list(stack),
            "visited": set(visited),
            "seen": set(seen)
        }

        u = stack.pop()
        visited.add(u)

        yield {
            "algo": "DFS",
            "action": "visit",
            "node": u,
            "stack": list(stack),
            "visited": set(visited),
            "seen": set(seen)
        }

        for v, _ in reversed(graph[u]):
            if v not in seen:
                seen.add(v)
                stack.append(v)

                yield {
                    "algo": "DFS",
                    "action": "edge",
                    "edge": (u, v),
                    "stack": list(stack),
                    "visited": set(visited),
                    "seen": set(seen)
                }
