import json
from flask import Blueprint, request, jsonify, Response
from app.database import db
from app.models import CommentList

comment_bp = Blueprint("comment", __name__)

# 댓글 추가(POST /comments/add)
# 입력: JSON 형식으로 게시글 ID, 댓글 내용, 작성자
@comment_bp.route("/comments/add", methods=["POST"])
def add_comment():
    """새 댓글 추가"""
    data = request.json
    post_id = data.get("post_id")
    content = data.get("content")
    author = data.get("author")

    if not all([post_id, content, author]):
        return jsonify({"error": "Missing required fields!"}), 400

    new_comment = CommentList(post_id=post_id, content=content, author=author)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({"message": f"Comment added to post {post_id}!", "id": new_comment.id}), 201


# 특정 게시글의 댓글 조회 (GET /comments/<post_id>)
# 반환: JSON 형식으로 댓글 ID, 내용, 작성자, 작성시간
@comment_bp.route("/comments/<int:post_id>", methods=["GET"])
def get_comments(post_id):
    """특정 게시글의 댓글 조회"""

    comments = CommentList.query.filter_by(post_id=post_id).all()

    if not comments:
        return jsonify({"error": "해당 게시글에 대한 댓글이 없습니다."}), 404

    result = [
        {
            "id": c.id,
            "content": c.content,
            "author": c.author,
            "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for c in comments
    ]

    return Response(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8")


# 특정 댓글 삭제(DELETE /comments/<comment_id>)
@comment_bp.route("/comments/<int:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    """특정 댓글 삭제"""
    comment = CommentList.query.get(comment_id)

    if not comment:
        return jsonify({"error": "Comment not found!"}), 404

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"message": f"Comment {comment_id} deleted!"})