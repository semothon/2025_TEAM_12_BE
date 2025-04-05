import heapq

def find_shortest_path(start, end, graph):
    """
    다익스트라 알고리즘을 이용해 최단 경로를 찾는 함수

    :param start: 시작 노드 이름
    :param end: 도착 노드 이름
    :param graph: {노드: {연결된_노드: 거리}} 형태의 딕셔너리
    :return: (최단 거리, 최단 경로 리스트)
    """
    # 우선순위 큐 (거리, 노드, 경로)
    pq = [(0, start, [])]
    
    # 방문한 노드
    visited = set()

    while pq:
        current_distance, current_node, path = heapq.heappop(pq)

        # 현재 노드를 방문했으면 건너뜀
        if current_node in visited:
            continue
        visited.add(current_node)

        # 현재 경로에 현재 노드 추가
        path = path + [current_node]

        # 목적지 도착 시 종료
        if current_node == end:
            return current_distance, path

        # 인접한 노드들 탐색
        for neighbor, distance in graph.get(current_node, {}).items():
            if neighbor not in visited:
                heapq.heappush(pq, (current_distance + distance, neighbor, path))

    return float('inf'), []  # 도달 불가능한 경우
