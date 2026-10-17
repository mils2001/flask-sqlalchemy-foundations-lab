
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


def earthquake_to_dict(earthquake):
    return {
        "id": earthquake.id,
        "magnitude": earthquake.magnitude,
        "location": earthquake.location,
        "year": earthquake.year,
    }


@app.route("/")
def index():
    return make_response({"message": "Flask SQLAlchemy Lab 1"}, 200)


@app.route("/earthquakes/<int:id>")
def earthquake_by_id(id):
    earthquake = db.session.get(Earthquake, id)

    if earthquake is None:
        return make_response(
            {"message": f"Earthquake {id} not found."}, 404
        )

    return make_response(earthquake_to_dict(earthquake), 200)


@app.route("/earthquakes/magnitude/<float:magnitude>")
def earthquakes_by_magnitude(magnitude):
    earthquakes = (
        Earthquake.query
        .filter(Earthquake.magnitude >= magnitude)
        .order_by(Earthquake.id)
        .all()
    )

    response = [earthquake_to_dict(earthquake) for earthquake in earthquakes]
    return make_response(response, 200)


@app.route("/earthquakes/magnitude")
def earthquakes_by_magnitude_query():
    from flask import request

    magnitude = request.args.get("magnitude", type=float)

    if magnitude is None:
        return make_response({"message": "Magnitude is required."}, 400)

    earthquakes = (
        Earthquake.query
        .filter(Earthquake.magnitude >= magnitude)
        .order_by(Earthquake.id)
        .all()
    )

    response = [earthquake_to_dict(earthquake) for earthquake in earthquakes]
    return make_response(response, 200)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
