from datetime import datetime
from dateutil.relativedelta import relativedelta
from project import db
from project.config import MAX_USERNAME_LENGTH, DATE_OF_BIRTH_KEY


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(MAX_USERNAME_LENGTH), unique=True)
    date_of_birth = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, date_of_birth):
        self.username = username
        self.date_of_birth = date_of_birth

    def __repr__(self):
        return '{ "username": "%s", "%s": "%s" }' % (self.username, DATE_OF_BIRTH_KEY, self.date_of_birth)

    def get_days_to_next_birthday(self):
        now = datetime.strptime(
            datetime.now().strftime("%Y-%m-%d"), '%Y-%m-%d')
        next_birthday = datetime(
            now.year, self.date_of_birth.month, self.date_of_birth.day)
        diff = next_birthday - now
        if diff.days < 0:
            diff = next_birthday + relativedelta(years=1) - now
        return diff.days
