import json
from flask import Blueprint, request, jsonify, Response
from app.database import db
from werkzeug.utils import secure_filename
from app.models import Files
from app.database import db
import os

upload_bp = Blueprint("upload", __name__)

@upload_bp.route('/upload_files', methods=["POST"])
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

    db.session.add(new_file)
    db.session.commit()

    return jsonify({"message": "파일 업로드 성공!", "path": new_file.path})