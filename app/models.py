from app.database import db

# 건물 테이블 (Building)
class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)  # 건물명
    classrooms = db.relationship("Classroom", backref="building", lazy=True)  # 1:N 관계

# 강의실 테이블 (Classroom)
class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # 강의실 이름
    floor = db.Column(db.String(20), nullable=False)  # 층수
    code = db.Column(db.String(50), unique=True, nullable=False)  # 강의실 특정 코드
    building_id = db.Column(db.Integer, db.ForeignKey("building.id"), nullable=False)  # 건물 테이블 참조 (FK)

# 연합 테이블 (Coalition)
class Coalition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    coalition_lists = db.relationship("CoalitionList", backref="coalition", lazy=True)

# 연합 목록 테이블 (CoalitionList)
class CoalitionList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    what_type = db.Column(db.String(50), nullable=False)
    coalition_id = db.Column(db.Integer, db.ForeignKey("coalition.id"), nullable=False)  # 연합 테이블 참조 (FK)
