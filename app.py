from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required
from models import db, Utilisateur
from routes_auth import auth_bp
from routes_exam import exam_bp

app = Flask(__name__)

# ================= CONFIGURATION =================
app.config['SECRET_KEY'] = 'dff0de101b446534f9f95d2dcec1f84a3ed9e046eec83e7d08cb425bd0ad4f62'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/gestion_concours_qcm?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ================= DATABASE =================
db.init_app(app)

# ================= LOGIN MANAGER =================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

# ================= BLUEPRINT =================
app.register_blueprint(auth_bp, url_prefix="/auth") 
app.register_blueprint(exam_bp)

# ================= ROUTES =================
@app.route("/")
def index():
    # Redirige vers login ou dashboard principal
    return redirect(url_for("auth.login"))

@app.route("/dashboard_admin")
@login_required
def dashboard_admin():
    return render_template("dashboard_admin.html", title="Dashboard Admin")

@app.route("/dashboard_enseignant")
@login_required
def dashboard_enseignant():
    return render_template("dashboard_enseignant.html", title="Dashboard Enseignant")

@app.route("/dashboard_candidat")
@login_required
def dashboard_candidat():
    return render_template("dashboard_candidat.html", title="Dashboard Candidat")

# ================= MAIN =================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # crée les tables si elles n'existent pas
    app.run(debug=True)