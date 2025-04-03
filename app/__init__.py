from flask import Flask
from app.database import db
from app.routes import main_bp
from app.post import post_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(post_bp)

    with app.app_context():
        db.create_all()

    return app
