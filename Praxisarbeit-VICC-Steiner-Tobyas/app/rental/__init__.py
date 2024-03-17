from flask import Blueprint

bp = Blueprint("rental", __name__)

from app.rental import routes  # noqa: E402, F401
