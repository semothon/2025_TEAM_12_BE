from app import create_app
from app.database import db
from app.models import Node, Edge

def insert_nodes_and_edges():

    # 🔴 기존 데이터 삭제 (중복 방지)
    db.session.query(Edge).delete()
    db.session.query(Node).delete()
    db.session.commit()

    nodes = ["정문", "공대", "외대", "멀관", "체대", "생대", "중도", 
             "커브길", "사색의 광장", "예대", "국제대", "전정대"]

    # 🔹 노드 추가 (중복 체크)
    node_objs = {}
    for name in nodes:
        existing_node = Node.query.filter_by(name=name).first()
        if not existing_node:
            node = Node(name=name)
            db.session.add(node)
            db.session.flush()  # ID 미리 받기
            node_objs[name] = node
        else:
            node_objs[name] = existing_node

    db.session.commit()

    # 🔹 간선 추가 (거리, 사용 가능 여부 포함)
    edges = [
        ("정문", "공대", 280, 0),
        ("정문", "외대", 300, 0),
        ("정문", "멀관", 485, 0),
        ("공대", "외대", 340, 0),
        ("외대", "멀관", 170, 0),
        ("외대", "체대", 160, 0),
        ("외대", "생대", 330, 0),
        ("멀관", "중도", 570, 0),
        ("생대", "중도", 290, 0),
        ("생대", "커브길", 160, 0),
        ("중도", "사색의 광장", 200, 0),
        ("중도", "국제대", 190, 0),
        ("커브길", "사색의 광장", 180, 0),
        ("사색의 광장", "예대", 260, 0),
        ("사색의 광장", "국제대", 170, 0),
        ("사색의 광장", "전정대", 210, 0),
        ("예대", "전정대", 240, 0),
        ("국제대", "전정대", 210, 0)
    ]


    for start, end, distance, status in edges:
        if start in node_objs and end in node_objs:
            edge = Edge(
                start_id=node_objs[start].id,
                end_id=node_objs[end].id,
                distance=distance,
                status=status  # 🔹 상태 추가
            )
            db.session.add(edge)

            # 🔹 양방향 간선 추가
            reverse_edge = Edge(
                start_id=node_objs[end].id,
                end_id=node_objs[start].id,
                distance=distance,
                status=status  # 🔹 상태 동일 적용
            )
            db.session.add(reverse_edge)

    db.session.commit()
    print("✅ 노드 및 간선 데이터 삽입 완료!")


# 🔹 Flask 앱 컨텍스트 내에서 실행
app = create_app()
with app.app_context():
    insert_nodes_and_edges()
