import pytest
from datetime import datetime
from project import db
from project.models import User
from sqlalchemy import func
from tests.utils import recreate_db

@pytest.mark.usefixtures("db")
class TestUser:
    
    def test_new_user(self):
        recreate_db()
        username = "foo"
        birthday = datetime.strptime(datetime.now().strftime("%Y-%m-%d"), '%Y-%m-%d')
        user = User(username, birthday)
        db.session.add(user)
        db.session.commit()
        assert user.username == username
        assert user.date_of_birth == birthday
        assert user.id > 0
        assert db.session.query(func.count(User.id)).scalar() == 1

    def test_update_user(self):
        recreate_db()
        username = "foo"
        birthday1 = datetime.strptime('2019-08-01', '%Y-%m-%d')
        db.session.add(User(username, birthday1))
        db.session.commit()
        user = User.query.filter_by(username=username).first()
        assert user.date_of_birth == birthday1
        assert user.id > 0
        assert db.session.query(func.count(User.id)).scalar() == 1
        
        birthday2 = datetime.strptime('2019-08-02', '%Y-%m-%d')
        user.date_of_birth = birthday2 
        db.session.commit()
        assert user.date_of_birth == birthday2
        assert user.id > 0
        assert db.session.query(func.count(User.id)).scalar() == 1
