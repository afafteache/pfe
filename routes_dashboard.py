from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/admin")
@login_required
def admin():
    if current_user.role != "admin":
        abort(403)
    return render_template("pages/dashboard_admin.html")


@dashboard_bp.route("/enseignant")
@login_required
def enseignant():
    if current_user.role != "enseignant":
        abort(403)
    return render_template("pages/dashboard_enseignant.html")


@dashboard_bp.route("/candidat")
@login_required
def candidat():
    if current_user.role != "candidat":
        abort(403)
    return render_template("pages/dashboard_candidat.html")
def candidat():
    return render_template("dashboard/candidat.html")