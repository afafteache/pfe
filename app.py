from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from models import db, Utilisateur

from routes_auth import auth_bp
from routes_exam import exam_bp
from routes_pages import pages_bp
from routes_dashboard import dashboard_bp  # ⚡ Assure-toi d’avoir ce fichier

app = Flask(__name__)

# ================= CONFIG =================
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/gestion_concours_qcm?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ================= DB =================
db.init_app(app)

# ================= LOGIN =================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

# ================= BLUEPRINTS =================
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(exam_bp, url_prefix="/exam")
app.register_blueprint(pages_bp, url_prefix="/pages")
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

# ================= ROOT =================
@app.route("/")
def home():
    # ⚡ Affiche directement la landing page
    return render_template("pages/landing.html")

# ================= MAIN =================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
