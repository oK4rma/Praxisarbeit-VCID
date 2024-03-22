import logging
import os
from flask import Flask
from flask_apidoc import ApiDoc
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler
from sqlalchemy import select
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
# Bestimmt die Ansicht, die für nicht authentifizierte Benutzer angezeigt wird.
login.login_view = "auth.login"  # type: ignore
doc = ApiDoc()

# Erstellt und konfiguriert die Flask-Anwendung.
def create_app(config=Config):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # Lädt die Konfiguration.
    app.config.from_object(config)

    # Initialisiert Erweiterungen mit der Anwendung.
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Importiert und registriert Blueprints für verschiedene Anwendungsteile
    from app import models
    from app.errors import bp as errors_bp
    # Registriert das Blueprint für Fehlerbehandlung.
    app.register_blueprint(errors_bp)

    from app.rental import bp as rental_bp
    # Registriert das Blueprint für Mietvorgänge.
    app.register_blueprint(rental_bp)

    from app.auth import bp as auth_bp
    # Registriert das Blueprint für Authentifizierung.
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.api import bp as api_bp
    # Registriert das Blueprint für die API.
    app.register_blueprint(api_bp, url_prefix="/api")

    # Konfiguriert das Logging.
    if not app.debug and not app.testing:
        if app.config["LOG_TO_STDOUT"]:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists("logs"):
                os.mkdir("logs")
            file_handler = RotatingFileHandler(
                "logs/rental.log", maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s "
                    "[in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("App startup")

    # Erstellt alle Datenbanktabellen, wenn nicht im Testmodus.
    if not app.testing:
        with app.app_context():
            # Create all database tables
            db.create_all()

            # Initialisiert Standard-Fahrzeuge, falls noch keine vorhanden sind.
            if not db.session.execute(select(models.rentalvehicle)).first():
                # Create default rental vehicles
                for x in range(1, 4):
                    vehicle = models.rentalvehicle(id=x, price=0, info=f"vehicles {x}")
                    db.session.add(vehicle)
                db.session.commit()
    # Gibt die konfigurierte Flask-Anwendung zurück.
    return app
