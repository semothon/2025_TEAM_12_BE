import json
from flask import Blueprint, request, jsonify, Response
from app.database import db
from app.models import TipList

tip_bp = Blueprint("tip", __name__)

@tip_bp.route("/tips", methods=["GET"])
def get_tip():

    building_id = request.args.get("building_id", type=int)

    if building_id:
        tips = TipList.query.filter_by(building_id=building_id).all()
    else:
        tips = TipList.query.filter_by(building_id=0).all() # 공통 tips : building_id == 0

    result = [
        {
            "id": t.id,
            "content": t.content,
            "building_id": t.building_id
        }
        for t in tips
    ]

    return Response(json.dumps(result, ensure_ascii=False),content_type="application/json; charset=utf-8")
