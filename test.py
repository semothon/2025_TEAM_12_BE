
from app import create_app
from app.database import db
from app.models import Building, Coalition, CoalitionList, Classroom

app = create_app()

def add_building(name):
    """새 건물 추가 (건물 유형 포함)"""
    name = name.split(' ')
    if len(name) == 1:
        with app.app_context():
            building = Building(name=name[0])
            db.session.add(building)
            db.session.commit()
            print(f"added: {building.name}")
    else:
        with app.app_context():
            building = Building(name=name[0], pictures=name[1])
            db.session.add(building)
            db.session.commit()
            print(f"added: {building.name}")

def add_sub_building(building_id, name, floor, code):
    """세부 건물 추가 (특정 건물 안에 포함)"""
    with app.app_context():
        parent_building = Building.query.get(building_id)
        
        sub_building = Classroom(name=name, floor=floor, code = code, building_id=building_id)
        db.session.add(sub_building)
        db.session.commit()
        print(f"✅ Added Sub-Building: {sub_building.name} (Under {parent_building.name})")

def reset():
    app = create_app()

    with app.app_context():
        for i in range(51, 66):
            building = Classroom.query.get(i)  # ID가 1인 건물 조회
            if building:
                db.session.delete(building)
                db.session.commit()
                print("삭제 완료!")
            else:
                print("삭제할 데이터가 없음")

if __name__ == "__main__":
    # reset()
    while True:

        name = input("🏢 Enter building name: ")
        add_building(name)

    
        # building_id = 16
        # name = input("🏠 Enter sub-building name: ")
        # name = name.split(maxsplit=1)
        # add_sub_building(building_id, name[1], name[0][0], name[0])

