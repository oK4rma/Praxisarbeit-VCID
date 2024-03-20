from flask import jsonify
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth


@bp.route("/tokens", methods=["POST"])
@basic_auth.login_required
# Generiert einen Authentifizierungstoken für den aktuellen Benutzer (über Basic Authentifizierung).
def get_token():
    # Ruft das Token des aktuellen Benutzers ab.
    token = basic_auth.current_user().get_token()  # type: ignore
    # Speichert Änderungen in der Datenbank.
    db.session.commit()
    # Gibt das generierte Token als JSON-Antwort zurück.
    return jsonify({"token": token})


@bp.route("/tokens", methods=["DELETE"])
@token_auth.login_required
# Widerruft das Authentifizierungstoken des aktuellen Benutzers (über Token Authentifizierung).
def revoke_token():
    # Ruft die Funktion zum Widerrufen des Tokens des aktuellen Benutzers auf. 'type: ignore' unterdrückt Typenwarnungen.
    token_auth.current_user().revoke_token()  # type: ignore
    # Speichert Änderungen in der Datenbank.
    db.session.commit()
    # Gibt eine leere Antwort mit Statuscode 204 (No Content) zurück, um den erfolgreichen Widerruf anzuzeigen.
    return "", 204
