from app.database import db
from app.models import Building, Edge, Node  # Edge 모델 가져오기
from app import create_app  # Flask 앱 생성 함수 가져오기

def reset_edge_table():
    app = create_app()  # Flask 앱 생성
    with app.app_context():  # 애플리케이션 컨텍스
        
        Building.__table__.drop(db.engine)
        db.session.commit()

# 실행
reset_edge_table()
