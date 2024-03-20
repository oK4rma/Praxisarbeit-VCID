from flask import jsonify
from app.api import bp
from app.api.auth import token_auth
from app.models import Reservation, rentalvehicle, User

@bp.route("/reservations/<int:id>", methods=["GET"])
# Zugriff erfordert einen gültigen Token.
@token_auth.login_required
# Gibt die Details einer spezifischen Reservierung als JSON zurück. Wenn die ID nicht gefunden wird, wird ein 404-Fehler ausgegeben.
def get_reservation(id):
    return jsonify(Reservation.query.get_or_404(id).to_dict())


@bp.route("/reservations", methods=["GET"])
# Gibt eine Liste aller Reservierungen zurück.
def get_reservations():
    data = Reservation.to_collection_dict(Reservation.query)
    return jsonify(data)


@bp.route("/reservations/<int:id>/get_reservation_user", methods=["GET"])
# Zugriff erfordert einen gültigen Token.
@token_auth.login_required
# Holt die Benutzerdetails der Reservierung. Gibt einen 404-Fehler zurück, wenn die Reservierung oder der Benutzer nicht gefunden wird.
def get_reservation_user(id):
    reservation = Reservation.query.get_or_404(id)
    user = User.query.get_or_404(reservation.user_id)
    return jsonify(user.to_dict())


@bp.route("/reservations/<int:id>/get_reservation_vehicle", methods=["GET"])
# Zugriff erfordert einen gültigen Token.
@token_auth.login_required
# Gibt die Fahrzeugdetails einer spezifischen Reservierung zurück. Gibt einen 404-Fehler zurück, wenn die Reservierung oder das Fahrzeug nicht gefunden wird.
def get_reservation_vehicle(id):
    reservation = Reservation.query.get_or_404(id)
    vehicle = rentalvehicle.query.get_or_404(reservation.rental_vehicle_id)
    return jsonify(vehicle.to_dict())
