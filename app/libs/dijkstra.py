import heapq

def find_shortest_path(start, end, graph):
    """
    다익스트라 알고리즘을 이용해 최단 경로를 찾는 함수

    :param start: 시작 노드 이름
    :param end: 도착 노드 이름
    :param graph: {노드: {연결된_노드: (거리, 기타정보)}} 형태의 딕셔너리
    :return: (최단 거리, 최단 경로 리스트)
    """
    pq = [(0, start, [])]  # (누적 거리, 현재 노드, 경로)
    visited = set()

    while pq:
        current_distance, current_node, path = heapq.heappop(pq)

        if current_node in visited:
            continue
        visited.add(current_node)

        path = path + [current_node]

        if current_node == end:
            return current_distance, path

        for neighbor, value in graph.get(current_node, {}).items():
            distance = value[0]  # 거리만 추출
            if neighbor not in visited:
                heapq.heappush(pq, (current_distance + distance, neighbor, path))

    return float('inf'), []
