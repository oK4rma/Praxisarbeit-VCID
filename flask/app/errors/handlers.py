from flask import render_template, request
from app import db
from app.api.errors import error_response as api_error_response
from app.errors import bp

# Entscheidet, ob der Client eine JSON-Antwort bevorzugt, basierend auf den Accept-Headern der Anfrage.
def wants_json_response():
    return (
            request.accept_mimetypes["application/json"]
            >= request.accept_mimetypes["text/html"]
    )

 # Fehlerbehandlung für den Fall, dass eine Ressource nicht gefunden wird (404 Fehler).
@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        # Gibt eine JSON-Antwort für API-Clients zurück, falls bevorzugt.
        return api_error_response(404)
    # Gibt eine HTML-Seite für Browser-Clients zurück, die einen 404-Fehler darstellt.
    return render_template("pages/errors/404.html"), 404


@bp.app_errorhandler(500)
# Fehlerbehandlung für interne Serverfehler (500 Fehler).
def internal_error(error):
    # Macht Datenbanktransaktionen rückgängig, um die Datenintegrität zu wahren.
    db.session.rollback()
    # Gibt eine JSON-Antwort für API-Clients zurück, falls bevorzugt.
    if wants_json_response():
        # Gibt eine JSON-Antwort für API-Clients zurück, falls bevorzugt.
        return api_error_response(500)
    # Gibt eine HTML-Seite für Browser-Clients zurück, die einen 500-Fehler darstellt.
    return render_template("pages/errors/500.html"), 500
