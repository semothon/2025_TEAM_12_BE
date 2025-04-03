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

    building = Building.query.get(building_id)
    if not building:
        return jsonify({"error": "Building not found!"}), 404

    classroom = Classroom(name=name, floor=floor, code=code, building_id=building_id)
    db.session.add(classroom)
    db.session.commit()
    return jsonify({"message": f"Classroom {classroom.name} added under {building.name}!"}), 201

@main_bp.route("/buildings", methods=["GET"])
def get_buildings():
    """모든 건물 및 포함된 강의실 조회"""
    buildings = Building.query.all()
    result = [
        {
            "id": b.id,
            "name": b.name,
            "classrooms": [
                {"id": c.id, "name": c.name, "floor": c.floor, "code": c.code}
                for c in b.classrooms
            ],
        }
        for b in buildings
    ]
    return Response(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8")
