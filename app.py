from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_file
)

import os

from models import db, User, File

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from encryption import encrypt_file, decrypt_file
from hashing import calculate_file_hash
from ipfs_upload import upload_to_ipfs, download_from_ipfs


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

        return render_template(
            "result.html",
            title="Login Failed",
            heading="❌ Login Failed",
            message="Invalid username or password."
        )

    return render_template("login.html")


# Dashboard
@app.route("/dashboard")
def dashboard():

    files = File.query.order_by(
        File.uploaded_at.desc()
    ).all()

    return render_template(
        "dashboard.html",
        files=files
    )


# Register
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            return render_template(
                "result.html",
                title="Registration Failed",
                heading="❌ Username Already Exists",
                message="Please choose another username."
            )

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return render_template(
            "result.html",
            title="Registration Successful",
            heading="✅ Registration Successful",
            message="Your account has been created successfully."
        )

    return render_template("register.html")


# Upload encrypted file to IPFS
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        file = request.files["file"]

        if file and file.filename:

            upload_folder = "uploads"

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            # Make filename safe
            safe_filename = secure_filename(
                file.filename
            )

            # File paths
            original_path = os.path.join(
                upload_folder,
                safe_filename
            )

            encrypted_filename = (
                safe_filename + ".enc"
            )

            encrypted_path = os.path.join(
                upload_folder,
                encrypted_filename
            )

            # Save original file temporarily
            file.save(original_path)

            # Calculate SHA-256 hash
            file_hash = calculate_file_hash(
                original_path
            )

            # Encrypt file
            encrypt_file(
                original_path,
                encrypted_path
            )

            # Delete plaintext file
            os.remove(original_path)

            # Upload encrypted file to IPFS
            cid = upload_to_ipfs(
                encrypted_path
            )

            # Save file information in database
            new_file = File(
                original_filename=safe_filename,
                encrypted_filename=encrypted_filename,
                file_hash=file_hash,
                ipfs_cid=cid
            )

            db.session.add(new_file)
            db.session.commit()

            return render_template(
                "result.html",
                title="Upload Successful",
                heading="✅ File Uploaded Successfully!",
                message=(
                    "Your file was encrypted, hashed, "
                    "and uploaded to IPFS."
                ),
                cid=cid,
                file_hash=file_hash
            )

        return render_template(
            "result.html",
            title="Upload Failed",
            heading="❌ Upload Failed",
            message="Please select a file."
        )

    return render_template("upload.html")


# Download / Recover file from IPFS
@app.route("/download/<int:file_id>")
def download_file(file_id):

    # Find file in database
    stored_file = File.query.get_or_404(
        file_id
    )

    # Recovery folder
    recovery_folder = "recovered"

    os.makedirs(
        recovery_folder,
        exist_ok=True
    )

    # Temporary encrypted file
    encrypted_path = os.path.join(
        recovery_folder,
        stored_file.encrypted_filename
    )

    # Recovered original file
    recovered_path = os.path.join(
        recovery_folder,
        stored_file.original_filename
    )

    try:

        # Download encrypted file from IPFS
        download_from_ipfs(
            stored_file.ipfs_cid,
            encrypted_path
        )

        # Decrypt
        decrypt_file(
            encrypted_path,
            recovered_path
        )

        # Calculate recovered file hash
        recovered_hash = calculate_file_hash(
            recovered_path
        )

        # Verify file integrity
        if recovered_hash != stored_file.file_hash:

            if os.path.exists(encrypted_path):
                os.remove(encrypted_path)

            if os.path.exists(recovered_path):
                os.remove(recovered_path)

            return render_template(
                "result.html",
                title="Verification Failed",
                heading="❌ File Verification Failed",
                message=(
                    "The recovered file does not match "
                    "the original file."
                )
            )

        # Send recovered file
        return send_file(
            recovered_path,
            as_attachment=True,
            download_name=stored_file.original_filename
        )

    except Exception as error:

        if os.path.exists(encrypted_path):
            os.remove(encrypted_path)

        if os.path.exists(recovered_path):
            os.remove(recovered_path)

        return render_template(
            "result.html",
            title="Recovery Failed",
            heading="❌ File Recovery Failed",
            message=str(error)
        )


# Start application
if __name__ == "__main__":
    app.run(debug=True)