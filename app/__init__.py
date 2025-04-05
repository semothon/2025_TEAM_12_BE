from .models import Building, Classroom, Coalition, CoalitionList, Edge, Node
from .libs import find_shortest_path, load_graph_from_db, time_to_travel, image_to_base64
from .database import db

from flask import Flask
from app.database import db
from app.routes import main_bp
from app.post import post_bp
from app.upload import upload_bp
from app.comment import comment_bp
from app.tip import tip_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(tip_bp)
    app.register_blueprint(upload_bp)

    with app.app_context():
        db.create_all()

    return app
