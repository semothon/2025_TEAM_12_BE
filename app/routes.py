import json
from flask import Blueprint, request, jsonify, Response
from app.database import db
from app.models import Building, Classroom

main_bp = Blueprint("main", __name__)

@main_bp.route("/add_building", methods=["POST"])
def add_building():
    """새 건물 추가"""
    data = request.json
    new_building = Building(name=data["name"])
    db.session.add(new_building)
    db.session.commit()

    response=jsonify({"message": f"Building {new_building.name} added!"}), 201
    response.headers['Access-Control-Allow-Origin'] = '*' # CORS 설정
    return response

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

    building = Building.query.get(building_id)
    if not building:
        return jsonify({"error": "Building not found!"}), 404

    classroom = Classroom(name=name, floor=floor, code=code, building_id=building_id)
    db.session.add(classroom)
    db.session.commit()

    response = jsonify({"message": f"Classroom {classroom.name} added under {building.name}!"}), 201
    response.headers['Access-Control-Allow-Origin'] = '*' # CORS 설정
    return response


@main_bp.route("/buildings", methods=["GET"])
def get_buildings():
    """건물 및 강의실 조회 (개별 조회 가능)"""
    query_id = request.args.get("id")

    if query_id:
        parts = query_id.split("-")

        if len(parts) == 1:
            # 건물 ID만 주어진 경우
            building = Building.query.get(parts[0])
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
            response=Response(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8")
            response.headers['Access-Control-Allow-Origin'] = '*' # CORS 설정
            return response

        elif len(parts) == 2:
            # 건물ID-강의실ID 형식으로 요청된 경우
            building_id, classroom_id = parts
            classroom = Classroom.query.filter_by(id=classroom_id, building_id=building_id).first()
            if not classroom:
                return jsonify({"error": "Classroom not found!"}), 404

            result = {
                "id": classroom.id,
                "name": classroom.name,
                "floor": classroom.floor,
                "code": classroom.code,
                "building_id": classroom.building_id,
            }
            response=Response(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8")
            response.headers['Access-Control-Allow-Origin'] = '*' # CORS 설정
            return response

    # ID가 없는 경우 모든 건물 목록만 반환
    buildings = Building.query.all()
    result = [{"id": b.id, "name": b.name} for b in buildings]

    response=Response(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8")
    response.headers['Access-Control-Allow-Origin'] = '*' # CORS 설정
    return response


@main_bp.route("/navigate", methods=["GET", "POST"])
def navigate():
    return