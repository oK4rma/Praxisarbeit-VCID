import datetime
from flask import jsonify, abort
from app.api import bp
from app.api.auth import token_auth
from app.models import rentalvehicle

@bp.route("/vehicles/<int:id>", methods=["GET"])
@token_auth.login_required
# Gibt Informationen zu einem spezifischen Fahrzeug basierend auf der ID zurück.
def get_vehicle(id):
    return jsonify(rentalvehicle.query.get_or_404(id).to_dict())

@bp.route("/vehicles", methods=["GET"])
# Gibt eine Liste aller Fahrzeuge zurück.
def get_vehicles():
    data = rentalvehicle.to_collection_dict(rentalvehicle.query)
    return jsonify(data)

@bp.route("/vehicles/<int:id>/get_vehicle_reservations", methods=["GET"])
@token_auth.login_required
# Gibt alle Reservierungen für ein spezifisches Fahrzeug zurück.
def get_vehicle_reservations(id):
    vehicle = rentalvehicle.query.get_or_404(id)
    data = rentalvehicle.to_collection_dict(vehicle.reservations)
    return jsonify(data)

@bp.route("/vehicles/<int:id>/get_vehicle_reserved/<date>", methods=["GET"])
@token_auth.login_required
# Überprüft, ob ein Fahrzeug an einem bestimmten Datum reserviert ist.
def get_vehicle_reserved(id, date):
    try:
        # Versucht, das Datum in ein Date-Objekt umzuwandeln.
        dateObj = datetime.date.fromisoformat(date)
    except ValueError:
        # Gibt einen 404-Fehler zurück, wenn das Datum ungültig ist.
        abort(404)

    vehicle = rentalvehicle.query.get_or_404(id)
    # Überprüft, ob das Fahrzeug reserviert ist.
    reservation = vehicle.is_reserved(dateObj)
    if reservation:
        # Gibt True zurück, wenn das Fahrzeug reserviert ist.
        return jsonify(True)
        # Gibt False zurück, wenn das Fahrzeug nicht reserviert ist.
    return jsonify(False)
