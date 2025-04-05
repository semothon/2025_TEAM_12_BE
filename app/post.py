import json
from flask import Blueprint, request, jsonify, Response
from app.database import db
from app.models import PostList

post_bp = Blueprint("post", __name__)

# 게시글 추가 (POST /posts/add)
# 입력: JSON 형식으로 제목, 내용, 작성자
@post_bp.route("/posts/add", methods=["POST"])
def add_post():
    """새 게시글 추가"""
    data = request.json
    title = data.get("title")
    content = data.get("content")
    building_id = data.get("building_id")

    if not all([title, content, building_id]):
        return jsonify({"error": "Missing required fields!"}), 400

    new_post = PostList(title=title, content=content, building_id=building_id)
    db.session.add(new_post)
    db.session.commit()

    # return jsonify({"message": f"Post '{new_post.title}' created!", "id": new_post.id}), 201

    response = jsonify({"message": f"Post '{new_post.title}' created!", "id": new_post.id})
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


# 게시글 목록 조회 (GET /posts)
# 입력: 쿼리 파라미터로 building_id
# 출력: JSON 형식으로 게시글 목록
# building_id가 주어지면 해당 작성자의 게시글만 조회
@post_bp.route("/posts", methods=["GET"])
def get_posts():
    building_id = request.args.get("building_id")

    if building_id:
        posts = PostList.query.filter_by(building_id=building_id).all()
    else:
        posts = PostList.query.all()

    result = []
    for p in posts:
        result.append({
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "building_id": p.building_id,
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "images": [f"/files/{f.id}" for f in p.files]  # 이미지 파일을 받을 수 있는 URL
        })

    response = Response(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8")
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# 게시글 수정 (PUT /posts/<post_id>)
# 입력: JSON 형식으로 제목, 내용
@post_bp.route("/posts/update", methods=["PUT"])
def update_post():
    post_id = request.args.get("post_id", type=int)
    if not post_id:
        return jsonify({"error": "post_id 쿼리가 필요합니다."}), 400

    post = PostList.query.get(post_id)
    if not post:
        return jsonify({"error": "게시물 없음"}), 404

    data = request.json
    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)
    post.building_id = data.get("building_id", post.building_id)
    db.session.commit()

    response = jsonify({"message": f"Post '{post.title}' updated!"})
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# 게시글 삭제 (DELETE /posts/<post_id>)
@post_bp.route("/posts/delete", methods=["DELETE"])
def delete_post():
    post_id = request.args.get("post_id", type=int)
    if not post_id:
        return jsonify({"error": "post_id 쿼리가 필요합니다."}), 400
    post = PostList.query.get(post_id)
    if not post:
        return jsonify({"error": "게시물 없음"}), 404

    db.session.delete(post)
    db.session.commit()

    response = jsonify({"message": f"Post '{post.title}, post_id: {post_id}' deleted!"})
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
    return jsonify({"message": f"Post '{post.title}, post_id: {post_id}' deleted!"})


if __name__ == "__main__":
    import app
    app = app.create_app()  # create_app 함수가 있다면 사용 (Flask Factory Pattern)
    with app.app_context():
        new_post = PostList(
            title='울 학교 사진 보고가',
            content='ㅈㄱㄴ',
            building_id=2
        )
        db.session.add(new_post)
        db.session.commit()
