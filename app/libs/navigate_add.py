from app import create_app
from app.database import db
from app.models import Node, Edge

def insert_nodes_and_edges():

    # 🔴 기존 데이터 삭제 (중복 방지)
    db.session.query(Edge).delete()
    db.session.query(Node).delete()
    db.session.commit()

    nodes = ["정문", "공대", "외대", "멀관", "체대", "생대", "중도", "교차로1", "교차로2", "예대", "국제대", "전정대"]

    # 🔹 노드 추가 (중복 체크)
    node_objs = {}
    for name in nodes:
        existing_node = Node.query.filter_by(name=name).first()
        if not existing_node:  # 중복 방지
            node = Node(name=name)
            db.session.add(node)
            db.session.flush()  # ID를 미리 할당받기 위해 flush()
            node_objs[name] = node
        else:
            node_objs[name] = existing_node

    db.session.commit()

    # 🔹 간선 추가 (거리 정보)
    edges = [
        ("정문", "공대", 280), ("정문", "외대", 300),
        ("공대", "외대", 340), ("외대", "멀관", 170),
        ("외대", "체대", 160), ("외대", "생대", 330),
        ("멀관", "중도", 570), ("체대", "생대", 320),
        ("생대", "중도", 290), ("생대", "교차로1", 160),
        ("중도", "교차로2", 200), ("교차로1", "교차로2", 180),
        ("교차로2", "예대", 260), ("교차로2", "국제대", 170),
        ("교차로2", "전정대", 210), ("예대", "전정대", 240),
        ("국제대", "전정대", 210)
    ]

    for start, end, distance in edges:
        if start in node_objs and end in node_objs:
            edge = Edge(
                start_id=node_objs[start].id,
                end_id=node_objs[end].id,
                distance=distance
            )
            db.session.add(edge)
            
            # 🔹 양방향 연결 추가
            reverse_edge = Edge(
                start_id=node_objs[end].id,
                end_id=node_objs[start].id,
                distance=distance
            )
            db.session.add(reverse_edge)

    db.session.commit()
    print("✅ 노드 및 간선 데이터 삽입 완료!")

# 🔹 Flask 앱 컨텍스트 내에서 실행
app = create_app()
with app.app_context():
    insert_nodes_and_edges()
