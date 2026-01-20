import heapq

def dijkstra(graph, start):
    dist = {n: float("inf") for n in graph}
    prev = {n: None for n in graph}

    dist[start] = 0
    visited = set()
    seen = {start}
    pq = [(0, start)]

    while pq:
        yield {
            "algo": "Dijkstra",
            "action": "pq",
            "pq": list(pq),
            "dist": dict(dist),
            "prev": dict(prev),
            "visited": set(visited),
            "seen": set(seen)
        }

        d, u = heapq.heappop(pq)
        if u in visited:
            continue

        visited.add(u)

        yield {
            "algo": "Dijkstra",
            "action": "visit",
            "node": u,
            "pq": list(pq),
            "dist": dict(dist),
            "prev": dict(prev),
            "visited": set(visited),
            "seen": set(seen)
        }

        for v, w in graph[u]:
            if v in visited:
                continue

            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
                seen.add(v)

                yield {
                    "algo": "Dijkstra",
                    "action": "relax",
                    "edge": (u, v, w),
                    "pq": list(pq),
                    "dist": dict(dist),
                    "prev": dict(prev),
                    "visited": set(visited),
                    "seen": set(seen)
                }
