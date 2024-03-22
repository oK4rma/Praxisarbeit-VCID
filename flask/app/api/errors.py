from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

# Erstellt eine Fehlerantwort für eine schlechte Anfrage (400 Bad Request) mit einer benutzerdefinierten Nachricht.
def bad_request(message):
    return error_response(400, message)

# Erstellt eine allgemeine Fehlerantwort mit dem angegebenen Statuscode und optionaler Nachricht.
def error_response(status_code, message=None):
    # 'HTTP_STATUS_CODES' wird verwendet, um den Standardfehlertext basierend auf dem Statuscode zu erhalten.
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
    if message:
        # Wenn eine benutzerdefinierte Nachricht angegeben ist, füge sie dem Antwort-Objekt hinzu.
        payload["message"] = message
    # Konvertiert das Antwort-Objekt in JSON.
    response = jsonify(payload)
    # Setzt den HTTP-Statuscode der Antwort.
    response.status_code = status_code
    return response
