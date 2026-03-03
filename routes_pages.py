from flask import Blueprint, render_template
from flask_login import login_required

pages_bp = Blueprint("pages", __name__)

# Page principale (index du dashboard)
@pages_bp.route("/")
@login_required
def index():
    return render_template("pages/index.html")

@pages_bp.route("/profile")
@login_required
def profile():
    return render_template("pages/profile.html")

@pages_bp.route("/tables")
@login_required
def tables():
    return render_template("pages/tables.html")

@pages_bp.route("/billing")
@login_required
def billing():
    return render_template("pages/billing.html")

@pages_bp.route("/notifications")
@login_required
def notifications():
    return render_template("pages/notifications.html")

@pages_bp.route("/map")
@login_required
def map_page():
    return render_template("pages/map.html")

@pages_bp.route("/typography")
@login_required
def typography():
    return render_template("pages/typography.html")

@pages_bp.route("/rtl")
@login_required
def rtl():
    return render_template("pages/rtl.html")

@pages_bp.route("/virtual-reality")
@login_required
def virtual_reality():
    return render_template("pages/virtual-reality.html")

# ⚡ Ajout pour corriger le lien "Dynamic Tables" dans sidebar.html
@pages_bp.route("/dynamic_dt")
@login_required
def dynamic_dt():
    return render_template("pages/dyn_dt.html")

# ⚡ Ajout pour corriger le lien "Charts" dans sidebar.html
@pages_bp.route("/charts")
@login_required
def charts():
    return render_template("pages/charts.html")

# ⚡ Ajout pour corriger le lien "Icons" dans sidebar.html
@pages_bp.route("/icons")
@login_required
def icons():
    return render_template("pages/icons.html")