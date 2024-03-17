import datetime
from flask import jsonify, abort

from app.api import bp
from app.api.auth import token_auth
from app.models import rentalvehicle


@bp.route("/vehicles/<int:id>", methods=["GET"])
@token_auth.login_required
def get_vehicle(id):
    return jsonify(rentalvehicle.query.get_or_404(id).to_dict())


@bp.route("/vehicles", methods=["GET"])
def get_vehicles():
    data = rentalvehicle.to_collection_dict(rentalvehicle.query)
    return jsonify(data)


@bp.route("/vehicles/<int:id>/get_vehicle_reservations", methods=["GET"])
@token_auth.login_required
def get_vehicle_reservations(id):
    vehicle = rentalvehicle.query.get_or_404(id)
    data = rentalvehicle.to_collection_dict(vehicle.reservations)
    return jsonify(data)


@bp.route("/vehicles/<int:id>/get_vehicle_reserved/<date>", methods=["GET"])
@token_auth.login_required
def get_vehicle_reserved(id, date):
    try:
        dateObj = datetime.date.fromisoformat(date)
    except ValueError:
        abort(404)

    vehicle = rentalvehicle.query.get_or_404(id)
    reservation = vehicle.is_reserved(dateObj)
    if reservation:
        return jsonify(True)
    return jsonify(False)