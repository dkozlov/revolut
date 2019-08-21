from flask.cli import FlaskGroup
from project import create_app, db
import time

app = create_app()
cli = FlaskGroup(create_app=create_app)

# Wait for Postgres to be ready and initialize the DB
with app.app_context():
    count = 0
    while True:
        if count > 100:
            break
        count += 1
        try:
            db.create_all()
            db.session.commit()
            break
        except Exception as e:
            app.logger.info("Attempt #{}, error: {}".format(count, str(e)))
            time.sleep(0.1)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()
