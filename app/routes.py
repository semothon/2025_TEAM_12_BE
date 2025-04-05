import json
from flask import Blueprint, request, jsonify, Response
from app import load_graph_from_db, find_shortest_path
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
    result = [{"id": b.id, "name": b.name} for b in buildings]

    return Response(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8")

@main_bp.route("/navigate", methods=["GET", "POST"])
def navigate():
    App = app.create_app()
    with App.app_context():
        # DB에서 그래프 데이터 로드
        graph = load_graph_from_db(Edge)

        data = request.json
        start_node = data.get("start")
        end_node = data.get("end")
        
        shortest_distance, shortest_path = find_shortest_path(start_node, end_node, graph)

        print(f"최단 거리: {shortest_distance}")
        print(f"최단 경로: {' -> '.join(shortest_path)}")
    
    return "<p>chech console</p>"