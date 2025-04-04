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
    author = data.get("author")
    # 사진 추가해야 됨

    if not all([title, content, author]):
        return jsonify({"error": "Missing required fields!"}), 400

    new_post = PostList(title=title, content=content, author=author)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": f"Post '{new_post.title}' created!", "id": new_post.id}), 201

# 게시글 전체 조회 (GET /posts)
# 반환: JSON 형식으로 게시글 ID, 제목, 작성자, 작성시간
@post_bp.route("/posts", methods=["GET"])
def get_posts():
    posts = PostList.query.all()
    result = [
        {
            "id": p.id,
            "title": p.title,
            "author": p.author,
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for p in posts
    ]
    return Response(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8")



# 특정 게시글 조회 (GET /posts/<post_id>)
# 반환: jSON 형식으로 게시글 ID, 제목, 내용, 작성자, 작성시간
@post_bp.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = PostList.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found!"}), 404

    result = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author": post.author,
        "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }

    return Response(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8")


# 게시글 수정 (PUT /posts/<post_id>)
# 입력: JSON 형식으로 제목, 내용
@post_bp.route("/posts/update/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    post = PostList.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found!"}), 404

    data = request.json
    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)
    db.session.commit()

    return jsonify({"message": f"Post '{post.title}' updated!"})


# 게시글 삭제 (DELETE /posts/<post_id>)
@post_bp.route("/posts/delete/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = PostList.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found!"}), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": f"Post '{post.title}, post_id: {post_id}' deleted!"})
