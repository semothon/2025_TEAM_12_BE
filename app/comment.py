import json
from flask import Blueprint, request, jsonify, Response
from app.database import db
from app.models import CommentList

comment_bp = Blueprint("comment", __name__)


# 댓글 추가 (POST /comments/add)
# 입력: 쿼리 파라미터로 post_id (게시글 ID)
# 입력: JSON 형식으로 내용, 작성자
@comment_bp.route("/comments/add", methods=["POST"])
def add_comment():
    """새 댓글 추가"""
    post_id = request.args.get("post_id", type=int)
    data = request.json
    content = data.get("content")
    author = data.get("author")

    if not all([post_id, content, author]):
        return jsonify({"error": "Missing required fields!"}), 400

    new_comment = CommentList(post_id=post_id, content=content, author=author)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({"message": f"Comment added to post {post_id}!", "comment_id": new_comment.id}), 201



# 댓글 목록 조회 (GET /comments)
# 입력: 쿼리 파라미터로 post_id (게시글 ID)
@comment_bp.route("/comments", methods=["GET"])
def get_comments():
    """특정 게시글의 댓글 조회"""
    post_id = request.args.get("post_id", type=int)
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
@comment_bp.route("/comments", methods=["DELETE"])
def delete_comment():
    """특정 댓글 삭제"""
    comment_id = request.args.get("comment_id", type=int)
    if not comment_id:
        return jsonify({"error": "comment_id 쿼리가 필요합니다."}), 400

    comment = CommentList.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found!"}), 404

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"message": f"Comment {comment_id} deleted!"})