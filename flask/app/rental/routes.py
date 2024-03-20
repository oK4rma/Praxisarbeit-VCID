import datetime
from flask import flash, redirect, render_template, url_for, abort
from flask_login import current_user, login_required
from sqlalchemy import select
from app import db
from app.models import rentalvehicle, Reservation, User
from app.rental import bp
from app.rental.calendar import rentalCalendar
from app.rental.forms import BaseForm

# Erstellt eine Instanz von rentalCalendar für die Verwendung in den Routen.
Calendar = rentalCalendar()


@bp.route("/")
@login_required
# Zeigt die Hauptseite der Anwendung an, inklusive eines Kalenders und verfügbarer Fahrzeuge.
def index():
    # Erstellt ein Basisformular für mögliche Aktionen auf der Seite.
    form = BaseForm()
    
    # Ermittelt das aktuelle Datum und teilt es in Jahr, Monat und den heutigen Tag auf.
    year = datetime.date.today().year
    month = datetime.date.today().month
    today = datetime.date.today()

    # Ruft alle verfügbaren Fahrzeuge aus der Datenbank ab.
    vehicles = db.session.scalars(select(rentalvehicle))

    # Gibt die Hauptseite mit den entsprechenden Daten für das Rendering zurück.
    return render_template(
        "pages/index.html",
        title="Home",
        year=year,
        month=month,
        activeDate=today,
        today=today,
        # Ruft Kalendertage für den aktuellen Monat ab.
        weeks=Calendar.get_days(month, year),
        vehicles=vehicles,
        form=form,
    )


@bp.route("/rental/<date>")
@login_required
# Zeigt die Hauptseite für ein spezifisches Datum an, ermöglicht die Anzeige von Fahrzeugreservierungen.
def date(date):
    # Erstellt erneut ein Basisformular.
    form = BaseForm()
    try:
        # Versucht, das übergebene Datum zu interpretieren.
        activeDate = datetime.date.fromisoformat(date)
    except ValueError:
        # Gibt einen 404 Fehler zurück, falls das Datum ungültig ist.
        abort(404)

    # Ermittelt das heutige Datum.
    today = datetime.date.today()
    # Verhindert die Anzeige für Daten in der Vergangenheit.
    if activeDate < today:
        abort(404)

    # Ermittelt Jahr und Monat des aktuellen Datums.
    year = datetime.date.today().year
    month = datetime.date.today().month
    # Ruft alle Fahrzeuge ab.
    vehicles = db.session.scalars(select(rentalvehicle))

    # Gibt die Seite mit den Daten für das angefragte Datum zurück.
    return render_template(
        "pages/index.html",
        title="Home",
        year=year,
        month=month,
        today=today,
        activeDate=activeDate,
        # Kalenderdaten für den Monat.
        weeks=Calendar.get_days(month, year),
        vehicles=vehicles,
        form=form,
    )


@bp.route("/reserve/<vehicle>/<day>", methods=["POST"])
@login_required
# Ermöglicht es, ein Fahrzeug für einen bestimmten Tag zu reservieren.
def reserve(vehicle, day):
    # Verwendet das Basisformular für die Reservierungsaktion.
    form = BaseForm()
    # Interpretiert das angegebene Datum.
    today = datetime.date.today()
    # Überprüft, ob das Formular korrekt abgesendet wurde.
    dayDate = datetime.date.fromisoformat(day)
    # Verhindert Reservierungen in der Vergangenheit.
    if form.validate_on_submit():
        if dayDate < today:
            flash("Cannot make reservations in the past")
            return redirect(url_for("rental.index"))

        # Sucht das spezifizierte Fahrzeug.
        vehicle = rentalvehicle.query.filter_by(id=vehicle).first()

        # Fehlerbehandlung, falls kein Fahrzeug gefunden wurde.
        if vehicle is None:
            flash(f"vehicles {vehicle} not found.")
            return redirect(url_for("rental.index"))

        # Sucht den aktuellen Benutzer.
        user = User.query.filter_by(id=current_user.id).first()  # type: ignore
        if user is None:
            raise ValueError("User not found")

        # Überprüft, ob bereits eine Reservierung für diesen Tag besteht.
        if user.reservation(dayDate):
            flash(
                "Cannot reserve vehicles. You can only have 1 vehicles per day", "error"
            )
            return redirect(url_for("rental.index"))

        # Führt die Reservierung durch.
        vehicle.reserve(dayDate, current_user)
        flash(f"vehicles {vehicle} reserved!")
        db.session.commit()

        return redirect(url_for("rental.index"))
    else:
        return redirect(url_for("rental.index"))


@bp.route("/free/<vehicle>/<day>", methods=["POST"])
@login_required
# Ermöglicht es, eine Reservierung für ein Fahrzeug an einem bestimmten Tag aufzuheben.
def free(vehicle, day):
    # Verwendet erneut das Basisformular für diese Aktion.
    form = BaseForm()
    # Interpretiert das angegebene Datum.
    today = datetime.date.today()
     # Überprüft, ob das Formular korrekt abgesendet wurde.
    dayDate = datetime.date.fromisoformat(day)
    # Verhindert Änderungen an Reservierungen in der Vergangenheit.
    if form.validate_on_submit():
        if dayDate < today:
            flash("Cannot make changes to reservations in the past")
            return redirect(url_for("rental.index"))

        # Sucht das spezifizierte Fahrzeug.
        vehicle = rentalvehicle.query.filter_by(id=vehicle).first()
        # Fehlerbehandlung, falls kein Fahrzeug gefunden wurde.
        if vehicle is None:
            flash(f"vehicles {vehicle} not found.")
            return redirect(url_for("rental.index"))

        # Versucht, die Reservierung aufzuheben.
        userReservation = vehicle.free(dayDate, current_user)
        # Falls erfolgreich, löscht die Reservierung aus der Datenbank.
        if userReservation is not None:
            db.session.delete(userReservation)
            db.session.commit()
            flash(f"vehicles {vehicle} is now free!")
        # Fehlermeldung, falls keine Reservierung für den Benutzer existiert.
        else:
            flash(f"vehicles {vehicle} is not reserved by you.", "error")
        return redirect(url_for("rental.index"))
    else:
        return redirect(url_for("rental.index"))


@bp.route("/accounting")
@login_required
# Zeigt die Kontoinformationsseite mit Übersicht der Fahrzeugreservierungen an.
def accounting():
    # Ruft alle Fahrzeuge ab.
    vehicles = db.session.scalars(select(rentalvehicle)).all()
    # Zählt die Fahrzeuge.
    vehicleCount = len(list(vehicles))
    # Ermittelt das heutige Datum.
    today = datetime.date.today()
    # Zählt belegte Fahrzeuge.
    occupied = len(list(filter(lambda x: x.is_reserved(today), vehicles)))
    # Berechnet die Belegungsrate.
    occupation = round((occupied / vehicleCount) * 100, 2)

    # Ruft alle Reservierungen bis zum heutigen Tag ab.
    reservations = db.session.scalars(
        select(Reservation)
        .filter(Reservation.date <= today)
        .join(rentalvehicle)
        .join(User)
    ).all()

    # Berechnet den Gesamterlös.
    revenue = sum(map(lambda x: x.rental_vehicle.price, reservations))

    # Gibt die Kontoseite mit den gesammelten Daten zurück.
    return render_template(
        "pages/accounting.html",
        title="Accounting",
        vehicles=vehicleCount,
        occupied=occupied,
        occupation=occupation,
        reservations=reservations,
        revenue=revenue,
    )
