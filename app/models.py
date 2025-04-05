from app.database import db

# 건물 테이블 (Building)
class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)  # 건물명
    pictures = db.Column(db.String(255), nullable=False)
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

class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    outgoing_edges = db.relationship(
        "Edge",
        foreign_keys="[Edge.start_id]",
        backref="start_node",
        lazy=True,
    )

    incoming_edges = db.relationship(
        "Edge",
        foreign_keys="[Edge.end_id]",
        backref="end_node",
        lazy=True,
    )


class Edge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_id = db.Column(db.Integer, db.ForeignKey("node.id"), nullable=False)
    end_id = db.Column(db.Integer, db.ForeignKey("node.id"), nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, default=0)



# 게시물 목록 테이블(post_list)
class PostList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    building_id = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, default=0)  # 좋아요 개수 추가

# 댓글 테이블(comment_list)
class CommentList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post_list.id"), nullable=False) # 게시물 ID 참조 (FK)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    post = db.relationship("PostList", backref=db.backref("comments", cascade="all, delete-orphan")) # 댓글과 게시물 간의 관계 설정

# tip 테이블
class TipList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    building_id = db.Column(db.Integer, nullable=False)

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post_list.id'), nullable=False)
    post = db.relationship('PostList', backref=db.backref('files', cascade="all, delete-orphan"))

class Tips(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255), nullable=True)
    building_id = db.Column(db.Integer, db.ForeignKey("building.id"), nullable=True) 