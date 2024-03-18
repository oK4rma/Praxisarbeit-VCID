import datetime
from flask import flash, redirect, render_template, url_for, abort
from flask_login import current_user, login_required
from sqlalchemy import select

from app import db
from app.models import rentalvehicle, Reservation, User
from app.rental import bp
from app.rental.calendar import rentalCalendar
from app.rental.forms import BaseForm

Calendar = rentalCalendar()


@bp.route("/")
@login_required
def index():
    form = BaseForm()

    year = datetime.date.today().year
    month = datetime.date.today().month
    today = datetime.date.today()

    vehicles = db.session.scalars(select(rentalvehicle))

    return render_template(
        "pages/index.html",
        title="Home",
        year=year,
        month=month,
        activeDate=today,
        today=today,
        weeks=Calendar.get_days(month, year),
        vehicles=vehicles,
        form=form,
    )


@bp.route("/rental/<date>")
@login_required
def date(date):
    form = BaseForm()
    try:
        activeDate = datetime.date.fromisoformat(date)
    except ValueError:
        abort(404)

    today = datetime.date.today()
    if activeDate < today:
        abort(404)

    year = datetime.date.today().year
    month = datetime.date.today().month
    vehicles = db.session.scalars(select(rentalvehicle))

    return render_template(
        "pages/index.html",
        title="Home",
        year=year,
        month=month,
        today=today,
        activeDate=activeDate,
        weeks=Calendar.get_days(month, year),
        vehicles=vehicles,
        form=form,
    )


@bp.route("/reserve/<vehicle>/<day>", methods=["POST"])
@login_required
def reserve(vehicle, day):
    form = BaseForm()
    today = datetime.date.today()
    dayDate = datetime.date.fromisoformat(day)
    if form.validate_on_submit():
        if dayDate < today:
            flash("Cannot make reservations in the past")
            return redirect(url_for("rental.index"))

        vehicle = rentalvehicle.query.filter_by(id=vehicle).first()

        if vehicle is None:
            flash(f"vehicles {vehicle} not found.")
            return redirect(url_for("rental.index"))

        user = User.query.filter_by(id=current_user.id).first()  # type: ignore
        if user is None:
            raise ValueError("User not found")

        if user.reservation(dayDate):
            flash(
                "Cannot reserve vehicles. You can only have 1 vehicles per day", "error"
            )
            return redirect(url_for("rental.index"))

        vehicle.reserve(dayDate, current_user)
        flash(f"vehicles {vehicle} reserved!")
        db.session.commit()

        return redirect(url_for("rental.index"))
    else:
        return redirect(url_for("rental.index"))


@bp.route("/free/<vehicle>/<day>", methods=["POST"])
@login_required
def free(vehicle, day):
    form = BaseForm()
    today = datetime.date.today()
    dayDate = datetime.date.fromisoformat(day)
    if form.validate_on_submit():
        if dayDate < today:
            flash("Cannot make changes to reservations in the past")
            return redirect(url_for("rental.index"))

        vehicle = rentalvehicle.query.filter_by(id=vehicle).first()
        if vehicle is None:
            flash(f"vehicles {vehicle} not found.")
            return redirect(url_for("rental.index"))

        userReservation = vehicle.free(dayDate, current_user)
        if userReservation is not None:
            db.session.delete(userReservation)
            db.session.commit()
            flash(f"vehicles {vehicle} is now free!")
        else:
            flash(f"vehicles {vehicle} is not reserved by you.", "error")
        return redirect(url_for("rental.index"))
    else:
        return redirect(url_for("rental.index"))


@bp.route("/accounting")
@login_required
def accounting():
    vehicles = db.session.scalars(select(rentalvehicle)).all()
    vehicleCount = len(list(vehicles))
    today = datetime.date.today()
    occupied = len(list(filter(lambda x: x.is_reserved(today), vehicles)))
    occupation = round((occupied / vehicleCount) * 100, 2)

    reservations = db.session.scalars(
        select(Reservation)
        .filter(Reservation.date <= today)
        .join(rentalvehicle)
        .join(User)
    ).all()

    revenue = sum(map(lambda x: x.rental_vehicle.price, reservations))

    return render_template(
        "pages/accounting.html",
        title="Accounting",
        vehicles=vehicleCount,
        occupied=occupied,
        occupation=occupation,
        reservations=reservations,
        revenue=revenue,
    )
