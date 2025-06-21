
from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db ,Hero,HeroPower,Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return '<h1>Hello World of Superheroes </h1>'

@app.route('/heroes')
def heroes():
    hero = [hero.to_dict() for hero in Hero.query.all()]
    return jsonify(hero), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)