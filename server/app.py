
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

#a. GET /heroes
@app.route('/heroes')
def heroes():
    heroes = [hero.to_dict() for hero in Hero.query.all()]
    return jsonify(heroes), 200

#b. GET /heroes/:id
@app.route('/heroes/<int:id>')
def heroById(id):
    hero = Hero.query.filter_by(id=id).first()
    if hero:
        return make_response(hero.to_dict(),200)
    else:
        return make_response({"error": "Hero not found"},404)

#c. GET /powers
@app.route('/powers')
def powers():
    powers = Power.query.all()
    return make_response([{"id": power.id, "description": power.description,"name": power.name,} for power in powers],200)

#d. GET /powers/<int:id>'
@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def powerById(id):
    power = Power.query.filter_by(id=id).first()
    if not power:
        return make_response({"error": "Power not found"}, 404)

    if request.method == 'GET':
        return make_response(power.to_dict(), 200)
    
    elif request.method == 'PATCH':
        try:
            data = request.get_json()

            new_description = data.get("description")
            if not new_description or len(new_description) < 20:
                return make_response({"errors": ["validation errors"]}, 400)

            power.description = new_description
            db.session.commit()
            return make_response(power.to_dict(), 200)

        except Exception as e:
            return make_response({"errors": [str(e)]}, 400)
        
#f. POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    # Validating strength value
    valid_strengths = ['Strong', 'Weak', 'Average']
    if strength not in valid_strengths:
        return make_response(jsonify({"errors": ["validation errors"]}), 400)

    # Check if Power and Hero exist
    power = Power.query.get(power_id)
    hero = Hero.query.get(hero_id)

    if not power or not hero:
        return make_response(jsonify({"errors": ["validation errors"]}), 400)

    
    hero_power = HeroPower(strength=strength, power=power, hero=hero)

    db.session.add(hero_power)
    db.session.commit()

    
    response_data = {
        "id": hero_power.id,
        "strength": hero_power.strength,
        "power_id": hero_power.power_id,
        "hero_id": hero_power.hero_id,
        "hero": {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name
        },
        "power": {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
    }

    return make_response(jsonify(response_data), 201)
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)