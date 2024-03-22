from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User


@bp.route("/login", methods=["GET", "POST"])
# Behandelt den Anmeldevorgang. Überprüft, ob der Benutzer bereits angemeldet ist.
def login():
    if current_user.is_authenticated:  # type: ignore
        # Benachrichtigung, dass der Benutzer bereits angemeldet ist.
        flash("Already logged in")
        # Weiterleitung zur Hauptseite.
        return redirect(url_for("rental.index"))

    # Erzeugt ein Anmeldeformular.
    form = LoginForm()
    # Überprüft, ob das Formular korrekt ausgefüllt wurde.
    if form.validate_on_submit():
        # Sucht nach dem Benutzer in der Datenbank.
        user = User.query.filter_by(username=form.username.data).first()
        # Überprüft, ob der Benutzer existiert und das Passwort korrekt ist.
        if user is None or not user.check_password(form.password.data):
            # Fehlermeldung bei ungültigen Anmeldedaten.
            flash("Invalid username or password", "error")
            # Rückleitung zur Anmeldeseite.
            return redirect(url_for("auth.login"))
        # Meldet den Benutzer an.
        login_user(user)
        # Holt den "next"-Parameter aus der URL, um nach der Anmeldung dorthin weiterzuleiten.
        next = request.args.get("next")
        # Sicherheitsüberprüfung, um Open Redirects zu vermeiden.
        if not next or url_parse(next).netloc != "":
            # Standardweiterleitung, falls "next" nicht gesetzt ist oder unsicher.
            next = url_for("rental.index")
        # Weiterleitung zur nächsten Seite.
        return redirect(next)
    # Zeigt die Anmeldeseite an.
    return render_template("pages/login.html", title="Sign In", form=form)


@bp.route("/logout")
# Meldet den Benutzer ab.
def logout():
    # Führt die Abmeldeprozedur aus.
    logout_user()
    # Weiterleitung zur Hauptseite.
    return redirect(url_for("rental.index"))


@bp.route("/register", methods=["GET", "POST"])
# Behandelt den Registrierungsvorgang. Überprüft, ob der Benutzer bereits angemeldet ist.
def register():
    if current_user.is_authenticated:  # type: ignore
        # Weiterleitung zur Hauptseite, falls bereits angemeldet.
        return redirect(url_for("rental.index"))
        # Erzeugt ein Registrierungsformular.
    form = RegistrationForm()
    # Überprüft, ob das Formular korrekt ausgefüllt wurde.
    if form.validate_on_submit():
        # Erstellt ein neues User-Objekt mit den eingegebenen Daten.
        user = User(username=form.username.data)  # type: ignore
        user.email = form.email.data
        # Setzt das Passwort (verschlüsselt).
        user.set_password(form.password.data)
        # Fügt den neuen Benutzer der Datenbank hinzu.
        db.session.add(user)
        # Speichert die Änderungen in der Datenbank.
        db.session.commit()
        # Bestätigungsnachricht.
        flash(f"Account created for {form.username.data}")
        # Weiterleitung zur Anmeldeseite.
        return redirect(url_for("auth.login"))
    # Zeigt die Registrierungsseite an.
    return render_template("pages/register.html", title="Register", form=form)
