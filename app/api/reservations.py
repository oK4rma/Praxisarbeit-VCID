from flask import jsonify

from app.api import bp
from app.api.auth import token_auth
from app.models import Reservation, rentalvehicle, User


@bp.route("/reservations/<int:id>", methods=["GET"])
@token_auth.login_required
def get_reservation(id):
    return jsonify(Reservation.query.get_or_404(id).to_dict())


@bp.route("/reservations", methods=["GET"])
def get_reservations():
    data = Reservation.to_collection_dict(Reservation.query)
    return jsonify(data)


@bp.route("/reservations/<int:id>/get_reservation_user", methods=["GET"])
@token_auth.login_required
def get_reservation_user(id):
    reservation = Reservation.query.get_or_404(id)
    user = User.query.get_or_404(reservation.user_id)
    return jsonify(user.to_dict())


@bp.route("/reservations/<int:id>/get_reservation_vehicle", methods=["GET"])
@token_auth.login_required
def get_reservation_vehicle(id):
    reservation = Reservation.query.get_or_404(id)
    vehicle = rentalvehicle.query.get_or_404(reservation.rental_vehicle_id)
    return jsonify(vehicle.to_dict())