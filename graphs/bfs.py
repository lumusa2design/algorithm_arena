from collections import deque

def bfs(graph, start):
    visited = set()
    seen = {start}
    queue = deque([start])

    while queue:
        yield {
            "algo": "BFS",
            "action": "queue",
            "queue": list(queue),
            "visited": set(visited),
            "seen": set(seen)
        }

        u = queue.popleft()
        visited.add(u)

        yield {
            "algo": "BFS",
            "action": "visit",
            "node": u,
            "queue": list(queue),
            "visited": set(visited),
            "seen": set(seen)
        }

        for v, _ in graph[u]:
            if v not in seen:
                seen.add(v)
                queue.append(v)

                yield {
                    "algo": "BFS",
                    "action": "edge",
                    "edge": (u, v),
                    "queue": list(queue),
                    "visited": set(visited),
                    "seen": set(seen)
                }
