from app import find_shortest_path, load_graph_from_db
from app.models import Edge
import app


# ✅ Flask 애플리케이션 컨텍스트 설정
app = app.create_app()
with app.app_context():
    # DB에서 그래프 데이터 로드
    graph = load_graph_from_db(Edge)

    # 최단 경로 찾기
    start_node = "정문"
    end_node = "멀관"
    shortest_distance, shortest_path = find_shortest_path(start_node, end_node, graph)

    print(f"최단 거리: {shortest_distance}")
    print(f"최단 경로: {' -> '.join(shortest_path)}")
