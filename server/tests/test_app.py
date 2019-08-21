from datetime import datetime
from project.models import User
from project import db
from sqlalchemy import func
from tests.utils import recreate_db, post_json, response_to_json 
from http import HTTPStatus

class TestFunctional:
    
    def test_metrics(self, client):
        recreate_db()
        response = client.get("/metrics")
        assert response.status_code == HTTPStatus.OK
    
    def test_healthz(self, client):
        response = client.get("/healthz")
        assert response.status_code == HTTPStatus.OK

    def test_readiness(self, client):
        response = client.get("/readiness")
        assert response.status_code == HTTPStatus.OK

    def test_new_user(self, client):
        recreate_db()
        username = "foo"
        birthday_string = "2019-01-01"
        birthday = datetime.strptime(birthday_string, '%Y-%m-%d')
        response = post_json(client, f'/hello/{username}', {"dateOfBirth": birthday_string})
        assert response.data == b''
        assert response.status_code == HTTPStatus.NO_CONTENT

        user = User.query.filter_by(username=username).first()
        assert user.date_of_birth == birthday
        assert user.id > 0
        assert db.session.query(func.count(User.id)).scalar() == 1
    
    def test_update_user(self, client):
        recreate_db()
        username = "foo"
        birthday_string = "2019-01-01"
        birthday = datetime.strptime(birthday_string, '%Y-%m-%d')
        response = post_json(client, f'/hello/{username}', {"dateOfBirth": birthday_string})
        assert response.data == b''
        assert response.status_code == HTTPStatus.NO_CONTENT

        user = User.query.filter_by(username=username).first()
        assert user.date_of_birth == birthday
        assert user.id > 0
        assert db.session.query(func.count(User.id)).scalar() == 1

        birthday2_string = "2019-01-02"
        birthday2 = datetime.strptime(birthday2_string, '%Y-%m-%d')
        response = post_json(client, f'/hello/{username}', {"dateOfBirth": birthday2_string})
        assert response.data == b''
        assert response.status_code == HTTPStatus.NO_CONTENT
        
        assert user.date_of_birth == birthday2
        assert user.id > 0
        assert db.session.query(func.count(User.id)).scalar() == 1
    
    def test_birthday(self, client):
        recreate_db()
        username = "foo"
        now = datetime.now()
        birthday_string = f'2000-{now.month}-{now.day}'
        birthday = datetime.strptime(birthday_string, '%Y-%m-%d')
        response = post_json(client, f'/hello/{username}', {"dateOfBirth": birthday_string})
        assert response.data == b''
        assert response.status_code == HTTPStatus.NO_CONTENT

        user = User.query.filter_by(username=username).first()
        assert user.date_of_birth == birthday
        assert user.id > 0
        assert db.session.query(func.count(User.id)).scalar() == 1

        response = client.get(f'/hello/{username}')
        assert response_to_json(response)['message'] == f'Hello, {username}! Happy birthday!'
        assert response.status_code == HTTPStatus.OK


    def test_birthday_is_in_several_days(self, client):
        recreate_db()
        username = "foo"
        now = datetime.now()
        birthday_string = f'2000-{now.month}-{now.day+1}'
        birthday = datetime.strptime(birthday_string, '%Y-%m-%d')
        response = post_json(client, f'/hello/{username}', {"dateOfBirth": birthday_string})
        assert response.data == b''
        assert response.status_code == HTTPStatus.NO_CONTENT

        user = User.query.filter_by(username=username).first()
        assert user.date_of_birth == birthday
        assert user.id > 0
        assert db.session.query(func.count(User.id)).scalar() == 1

        response = client.get(f'/hello/{username}')
        assert response_to_json(response)['message'] == f'Hello, foo! Your birthday is in 1 day(s)'
        assert response.status_code == HTTPStatus.OK
    
    def test_non_alphabetic_username(self, client):
        recreate_db()
        username = "foo1"
        birthday_string = "2019-01-01"
        birthday = datetime.strptime(birthday_string, '%Y-%m-%d')
        response = post_json(client, f'/hello/{username}', {"dateOfBirth": birthday_string})
        assert response_to_json(response)['message'] == f"Invalid username '{username}'. <username> must contains only letters"
        assert response.status_code == HTTPStatus.BAD_REQUEST
    
    def test_birthday_after_today_date(self, client):
        recreate_db()
        username = "foo"
        now = datetime.now()
        now_string = now.strftime("%Y-%m-%d")
        birthday_string = f'{now.year}-{now.month}-{now.day+1}'
        birthday = datetime.strptime(birthday_string, '%Y-%m-%d')
        response = post_json(client, f'/hello/{username}', {"dateOfBirth": birthday_string})
        assert response_to_json(response)['message'] == f"'{birthday_string}' date must be a date before the today date ('{now_string}')"
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_user_not_found(self, client):
        recreate_db()
        username = "foo"
        response = client.get(f'/hello/{username}')
        assert response_to_json(response)['message'] == f"User with name '{username}' not found"
        assert response.status_code == HTTPStatus.NOT_FOUND
