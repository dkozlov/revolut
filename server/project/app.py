from flask import Blueprint, request, jsonify
from flask import current_app as app
from flask_restful import Resource, abort
from http import HTTPStatus
from project import db, api
from project.config import MAX_USERNAME_LENGTH, DATE_OF_BIRTH_KEY
from project.models import User
from datetime import datetime
from sqlalchemy import func


app_blueprint = Blueprint('app', __name__)


def abort_if_username_is_not_valid(username):
    if not username.isalpha():
        abort(HTTPStatus.BAD_REQUEST,
              message="Invalid username '{}'. <username> must contains only letters".format(username))
    if len(username) > MAX_USERNAME_LENGTH:
        abort(HTTPStatus.BAD_REQUEST,
              message="<username> length must be less than {} letters"
              .format(MAX_USERNAME_LENGTH))


def abort_if_json_data_is_not_valid(json_data):
    if DATE_OF_BIRTH_KEY not in json_data:
        abort(HTTPStatus.BAD_REQUEST, message="{} key is missing in the JSON input".format(
            DATE_OF_BIRTH_KEY))


def abort_if_date_of_birth_is_not_valid(date_of_birth_string):
    try:
        date_of_birth = datetime.strptime(
            str(date_of_birth_string), '%Y-%m-%d')
        current_date = datetime.strptime(
            datetime.now().strftime("%Y-%m-%d"), '%Y-%m-%d')
        if date_of_birth >= current_date:
            abort(HTTPStatus.BAD_REQUEST, message="'{}' date must be a date before the today date ('{}')".format(
                date_of_birth_string, current_date.strftime("%Y-%m-%d")))
        return date_of_birth
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST,
              message="Incorrect data format for '{}' date, should be YYYY-MM-DD".format(date_of_birth_string))


class HelloWorld(Resource):
    def get(self, username):
        abort_if_username_is_not_valid(username)
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            app.logger.info("Found existing user: {}".format(existing_user))
            days = existing_user.get_days_to_next_birthday()
            if days > 0:
                return {'message': "Hello, {}! Your birthday is in {} day(s)".format(username, days)}, HTTPStatus.OK
            return {'message': "Hello, {}! Happy birthday!".format(username)}, HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND,
                  message="User with name '{}' not found".format(username))

    def put(self, username):
        abort_if_username_is_not_valid(username)
        try:
            json_data = request.get_json(force=True)
            abort_if_json_data_is_not_valid(json_data)
        except TypeError:
            abort(HTTPStatus.BAD_REQUEST, message="Invalid JSON input")
        date_of_birth = abort_if_date_of_birth_is_not_valid(
            json_data[DATE_OF_BIRTH_KEY])
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            app.logger.info("Found existing user: {}".format(existing_user))
            if existing_user.date_of_birth != date_of_birth:
                app.logger.info("Updating {} from '{}', to '{}' for user '{}'".format(
                    DATE_OF_BIRTH_KEY, existing_user.date_of_birth, date_of_birth, username))
                existing_user.date_of_birth = date_of_birth
            else:
                app.logger.info("Skipping update because the {} is not changed for user '{}'".format(
                    DATE_OF_BIRTH_KEY, username))
        else:
            new_user = User(username, date_of_birth)
            app.logger.info("Adding new user: {}".format(new_user))
            db.session.add(new_user)
        db.session.commit()
        return '', HTTPStatus.NO_CONTENT


@app_blueprint.route('/healthz')
def healthz():
    try:
        db.session.execute('SELECT 1')
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))
    return '', HTTPStatus.OK


@app_blueprint.route('/readiness')
def readiness():
    try:
        db.session.query(func.count(User.id)).scalar()
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))
    return '', HTTPStatus.OK


@app_blueprint.route('/metrics')
def metrics():
    try:
        return jsonify({'users_count': db.session.query(func.count(User.id)).scalar()}), HTTPStatus.OK
    except Exception as e:
        print(str(e))
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))


api.add_resource(HelloWorld, '/hello/<string:username>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
