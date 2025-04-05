import json
from flask import Blueprint, request, jsonify, Response
from app import load_graph_from_db, find_shortest_path, time_to_travel
from app.models import Edge
import app


main_bp = Blueprint("main", __name__)

@main_bp.route("/add_building", methods=["POST"])
def add_building():
    """새 건물 추가"""
    data = request.json
    new_building = app.Building(name=data["name"])
    app.db.session.add(new_building)
    app.db.session.commit()
    return jsonify({"message": f"Building {new_building.name} added!"}), 201

@main_bp.route("/add_classroom", methods=["POST"])
def add_classroom():
    """건물 내 강의실 추가"""
    data = request.json
    building_id = data.get("building_id")
    name = data.get("name")
    floor = data.get("floor")
    code = data.get("code")

    if not all([building_id, name, floor, code]):
        return jsonify({"error": "Missing required fields!"}), 400

    building = app.Building.query.get(building_id)
    if not building:
        return jsonify({"error": "Building not found!"}), 404

    classroom = app.Classroom(name=name, floor=floor, code=code, building_id=building_id)
    app.db.session.add(classroom)
    app.db.session.commit()
    return jsonify({"message": f"Classroom {classroom.name} added under {building.name}!"}), 201



@main_bp.route("/buildings", methods=["GET"])
def get_buildings():
    """건물 및 강의실 조회 (개별 조회 가능)"""
    query_id = request.args.get("id")

    if query_id:
        parts = query_id.split("-")

        if len(parts) == 1:
            # 건물 ID만 주어진 경우
            building = app.Building.query.get(parts[0])
            if not building:
                return jsonify({"error": "Building not found!"}), 404

            result = {
                "id": building.id,
                "name": building.name,
                "image": app.image_to_base64(building.pictures),
                "classrooms": [
                    {"id": c.id, "name": c.name, "floor": c.floor, "code": c.code}
                    for c in building.classrooms
                ],
            }
            return Response(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8")

        elif len(parts) == 2:
            # 건물ID-강의실ID 형식으로 요청된 경우
            building_id, classroom_id = parts
            classroom = app.Classroom.query.filter_by(id=classroom_id, building_id=building_id).first()
            if not classroom:
                return jsonify({"error": "Classroom not found!"}), 404

            result = {
                "id": classroom.id,
                "name": classroom.name,
                "floor": classroom.floor,
                "code": classroom.code,
                "building_id": classroom.building_id,
            }
            return Response(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8")

    # ID가 없는 경우 모든 건물 목록만 반환
    buildings = app.Building.query.all()
    result = [{
        "id": b.id,
        "name": b.name,
        # "image": app.image_to_base64(b.pictures)
    } for b in buildings]

    return Response(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8",headers={"Access-Control-Allow-Origin": "*"})

@main_bp.route("/navigate", methods=["GET", "POST"])
def navigate():
    App = app.create_app()
    with App.app_context():
        graph = load_graph_from_db(Edge)


        # ✅ 입력 받기: GET 쿼리 or POST JSON
        if request.method == "POST":
            data = request.get_json()
            start_node = data.get("start")
            end_node = data.get("end")
        else:  # GET
            start_node = request.args.get("start")
            end_node = request.args.get("end")

        # 입력값 검증
        if not start_node or not end_node:
            return Response(json.dumps({
                "status": "start와 end를 모두 지정해주세요."
            }, ensure_ascii=False), content_type="application/json; charset=utf-8"), 400


        def is_path_unavailable(path, graph):
            for i in range(len(path) - 1):
                from_node = path[i]
                to_node = path[i + 1]
                edge = graph.get(from_node, {}).get(to_node)
                if edge is None:
                    return True  # 경로가 없으면 unavailable로 간주
                _, under_construction = edge
                if under_construction == 1:  # 이용 불가능한 길
                    return True
            return False



        attempts = 0
        max_attempts = 20
        excluded_edges = set()

        shortest_distance = float('inf')
        shortest_path = []
        invalid_path = []

        while attempts < max_attempts:
            attempts += 1

            # 제외된 edge들을 제거한 graph 구성
            modified_graph = {
                node: {
                    neighbor: dist for neighbor, dist in neighbors.items()
                    if (node, neighbor) not in excluded_edges
                }
                for node, neighbors in graph.items()
            }

            distance, path = find_shortest_path(start_node, end_node, modified_graph)

            if distance == float('inf'):
                break  # 더 이상 경로 없음

            if is_path_unavailable(path, graph):
                # 음수 간선 포함 경로: 기록만 하고 제외
                if not invalid_path:
                    invalid_path = path
                for i in range(len(path) - 1):
                    excluded_edges.add((path[i], path[i + 1]))
                continue
            else:
                shortest_distance = distance
                shortest_path = path
                break

        result = {}

        if shortest_path:
            result.update({
                "path": shortest_path,
                "distance": shortest_distance,
                "time": time_to_travel(shortest_distance)
            })
            if invalid_path:
                result["status"] = "현재 사용할 수 없는 경로 제거됨"
                result["invalid_path"] = invalid_path
        elif invalid_path:
            result = {
                "path": invalid_path,
                "status": "이 길은 사용할 수 없습니다!",
                "distance": "N/A",
                "time": "N/A"
            }
        else:
            result = {
                "status": "도달 가능한 경로가 없습니다.",
                "path": [],
                "distance": "N/A",
                "time": "N/A"
            }

    return Response(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8", headers={"Access-Control-Allow-Origin": "*"})


@main_bp.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    chars = list(query)

    # DB에서 문자 포함 필터링
    building_query = app.Building.query
    for ch in chars:
        building_query = building_query.filter(app.Building.name.ilike(f"%{ch}%"))
    building_matches = building_query.all()

    classroom_query = app.Classroom.query
    for ch in chars:
        classroom_query = classroom_query.filter(
            (app.Classroom.name.ilike(f"%{ch}%")) |
            (app.Classroom.code.ilike(f"%{ch}%"))
        )
    classroom_matches = classroom_query.all()

    # 글자 겹침 수 계산 함수
    def count_overlap(name, query):
        return sum(name.count(ch) for ch in query)

    results = []

    for b in building_matches:
        score = count_overlap(b.name, query)
        results.append({
            "type": "building",
            "id": b.id,
            "name": b.name,
            "score": score
        })

    for c in classroom_matches:
        score = max(
            count_overlap(c.name, query),
            count_overlap(c.code, query)
        )
        results.append({
            "type": "classroom",
            "id": c.id,
            "name": c.name,
            "code": c.code,
            "floor": c.floor,
            "building": c.building.name,
            "score": score
        })

    # 점수 높은 순으로 정렬
    results.sort(key=lambda x: x["score"], reverse=True)

    # 점수 제거하고 반환
    for r in results:
        r.pop("score", None)

    return Response(json.dumps(results, ensure_ascii=False), content_type="application/json; charset=utf-8", headers={"Access-Control-Allow-Origin": "*"})

from flask import request, jsonify
from werkzeug.utils import secure_filename
from app.models import Files
import os
@main_bp.route('/upload_files', methods=["POST"])
def upload_files():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    f = request.files['file']
    if f.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(f.filename)
    upload_dir = os.path.join('statics', 'images')
    os.makedirs(upload_dir, exist_ok=True)  # 디렉토리 없으면 생성

    file_path = os.path.join(upload_dir, filename)
    f.save(file_path)

    # post_id는 임시로 1번 고정
    post_id = request.args.get('post_id')
    new_file = Files(path=f'/statics/images/{filename}', post_id=post_id)

    app.db.session.add(new_file)
    app.db.session.commit()

    return jsonify({"message": "파일 업로드 성공!", "path": new_file.path})


from flask import render_template_string
@main_bp.route("/test-autocomplete")
def test_page():
    return render_template_string(open("test.html", "r", encoding="utf-8").read())

from flask import render_template
@main_bp.route('/test-upload')
def test_upload():
    return render_template('test-upload.html')