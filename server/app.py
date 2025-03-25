#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, abort
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.filter_by(id=id).first()
    
    if earthquake is None:
        abort(404, description=f"Earthquake {id} not found.")
    
    return jsonify({
        "id": earthquake.id,
        "location": earthquake.location,
        "magnitude": earthquake.magnitude,
        "year": earthquake.year
    })

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"message": error.description}), 404

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    if not earthquakes:
        return jsonify({
            "count": 0,
            "quakes": [],
            "status": "success"
        }), 200
    return jsonify({
        "count": len(earthquakes),
        "quakes":[earthquake.to_dict() for earthquake in earthquakes],
        "status": "success"
    }),200



if __name__ == '__main__':
    app.run(port=5550, debug=True)
