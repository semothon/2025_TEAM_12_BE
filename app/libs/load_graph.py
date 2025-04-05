
def load_graph_from_db(someClass):
    """ 데이터베이스에서 그래프 데이터를 불러오는 함수 """
    graph = {}
    
    edges = someClass.query.all()
    for edge in edges:
        start = edge.start_node.name
        end = edge.end_node.name
        distance = edge.distance

        if start not in graph:
            graph[start] = {}
        graph[start][end] = distance

    return graph