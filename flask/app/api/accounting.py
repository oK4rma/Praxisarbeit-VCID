import datetime
from flask import jsonify
from sqlalchemy import select

from app import db
from app.api import bp
from app.api.auth import token_auth
from app.models import Reservation, rentalvehicle, User


@bp.route("/accounting", methods=["GET"])
@token_auth.login_required
def get_accounting():
    vehicles = db.session.scalars(select(rentalvehicle)).all()
    vehicleCount = len(list(vehicles))
    today = datetime.date.today()
    occupied = len(list(filter(lambda x: x.is_reserved(today), vehicles)))
    occupation = round((occupied / vehicleCount), 2)

    reservations = db.session.scalars(
        select(Reservation)
        .filter(Reservation.date <= today)
        .join(rentalvehicle)
        .join(User)
    ).all()

    revenue = sum(map(lambda x: x.rental_vehicle.price, reservations))
    return jsonify(
        {
            "vehicles": vehicleCount,
            "occupied": occupied,
            "occupation": occupation,
            "revenue": revenue,
        }
    )