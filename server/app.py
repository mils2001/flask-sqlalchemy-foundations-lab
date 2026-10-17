
#!/usr/bin/env python3

from flask import Flask, make_response, request
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)


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

    response = {
        "id": earthquake.id,
        "magnitude": earthquake.magnitude,
        "location": earthquake.location,
        "year": earthquake.year,
    }

    return make_response(response, 200)


@app.route("/earthquakes")
def earthquakes_by_magnitude():
    magnitude = request.args.get("magnitude", type=float)

    query = Earthquake.query

    if magnitude is not None:
        query = query.filter(Earthquake.magnitude >= magnitude)

    earthquakes = query.order_by(Earthquake.id).all()

    response = [
        {
            "id": earthquake.id,
            "magnitude": earthquake.magnitude,
            "location": earthquake.location,
            "year": earthquake.year,
        }
        for earthquake in earthquakes
    ]

    return make_response(response, 200)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
