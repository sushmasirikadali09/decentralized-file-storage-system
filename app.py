from flask import Flask, render_template, request, redirect, url_for
import os

from models import db, User, File

from werkzeug.security import generate_password_hash, check_password_hash

from encryption import encrypt_file
from hashing import calculate_file_hash
from ipfs_upload import upload_to_ipfs


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


# Login
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


# Dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# Register
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


# Encrypted file upload with SHA-256 hash and IPFS
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        file = request.files["file"]

        if file and file.filename:

            upload_folder = "uploads"

            os.makedirs(upload_folder, exist_ok=True)

            # File paths
            original_path = os.path.join(
                upload_folder,
                file.filename
            )

            encrypted_path = os.path.join(
                upload_folder,
                file.filename + ".enc"
            )

            # Save original file temporarily
            file.save(original_path)

            # Calculate SHA-256 hash
            file_hash = calculate_file_hash(original_path)

            # Encrypt the file
            encrypt_file(
                original_path,
                encrypted_path
            )

            # Delete original unencrypted file
            os.remove(original_path)

            # Upload encrypted file to IPFS
            cid = upload_to_ipfs(encrypted_path)

            # Save file information including CID
            new_file = File(
                original_filename=file.filename,
                encrypted_filename=file.filename + ".enc",
                file_hash=file_hash,
                ipfs_cid=cid
            )

            db.session.add(new_file)
            db.session.commit()

            return (
                "File encrypted, hashed, and uploaded to IPFS successfully!"
                "<br><br>"
                f"IPFS CID: {cid}"
                "<br><br>"
                "CID saved in database successfully!"
            )

    return render_template("upload.html")


# Start application
if __name__ == "__main__":
    app.run(debug=True)