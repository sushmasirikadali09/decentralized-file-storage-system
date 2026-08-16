from flask import Flask, render_template, request, redirect, url_for
import os
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///storage.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connect database to Flask
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Login page
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            return redirect(url_for("dashboard"))

        return "Invalid username or password!"

    return render_template("login.html")


# Dashboard page
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        file = request.files["file"]

        if file and file.filename:

            upload_folder = "uploads"

            os.makedirs(upload_folder, exist_ok=True)

            file_path = os.path.join(upload_folder, file.filename)

            file.save(file_path)

            return "File uploaded successfully!"

    return render_template("upload.html")

# Register page
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "Username already exists!"

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


# Start application
if __name__ == "__main__":
    app.run(debug=True)