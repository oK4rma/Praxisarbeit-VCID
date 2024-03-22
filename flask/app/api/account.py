import datetime
from flask import jsonify
from sqlalchemy import select
from app import db
from app.api import bp
from app.api.auth import token_auth
from app.models import Reservation, rentalvehicle, User

# Definiert eine Route '/account' für GET-Anfragen.
@bp.route("/account", methods=["GET"])
# Stellt sicher, dass der Benutzer authentifiziert sein muss, um auf diese Route zuzugreifen.
@token_auth.login_required
def get_account():
       # Ruft alle Fahrzeuge aus der Datenbank ab.
    vehicles = db.session.scalars(select(rentalvehicle)).all()
    # Zählt die Fahrzeuge.
    vehicleCount = len(list(vehicles))
    # Ermittelt das heutige Datum.
    today = datetime.date.today()
    # Zählt, wie viele Fahrzeuge heute reserviert sind.
    occupied = len(list(filter(lambda x: x.is_reserved(today), vehicles)))
    # Berechnet die Belegungsrate
    occupation = round((occupied / vehicleCount), 2)

    # Ruft alle Reservierungen ab, die bis heute erfolgt sind, inklusive Verknüpfungen zu Fahrzeugen und Benutzern.
    reservations = db.session.scalars(
        select(Reservation)
        .filter(Reservation.date <= today)
        .join(rentalvehicle)
        .join(User)
    ).all()

    # Gibt die Daten als JSON zurück.
    return jsonify(
        {
            "vehicles": vehicleCount,
            "occupied": occupied,
            "occupation": occupation,
            "revenue": revenue,
        }
    )
