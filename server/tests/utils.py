import json
from project import db

def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.put(url, data=json.dumps(json_dict), content_type='application/json')

def response_to_json(response):
    return json.loads(response.data.decode('utf8'))
