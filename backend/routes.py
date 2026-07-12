import os
import uuid

from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash,
    current_app,
    send_from_directory
)

from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from backend.database import db
from backend.models import User, Letter

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return redirect(url_for("main.login"))


@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["username"] = user.username
            return redirect(url_for("main.inbox"))

        flash("Username or Password is incorrect.", "danger")
        return redirect(url_for("main.login"))

    return render_template("login.html")


@main.route("/inbox")
def inbox():

    if "username" not in session:
        return redirect(url_for("main.login"))

    current_user = User.query.filter_by(
        username=session["username"]
    ).first()

    letters = Letter.query.filter_by(
        receiver_id=current_user.id
    ).order_by(
        Letter.created_at.desc()
    ).all()

    return render_template(
        "inbox.html",
        letters=letters,
        current_user=current_user
    )


@main.route("/compose", methods=["GET", "POST"])
def compose():

    if "username" not in session:
        return redirect(url_for("main.login"))

    users = User.query.filter(
        User.username != session["username"]
    ).all()

    if request.method == "POST":

        receiver_id = request.form.get("receiver")
        subject = request.form.get("subject")
        body = request.form.get("content")

        # دریافت فایل
        attachment = request.files.get("attachment")

        filename = None

        if attachment and attachment.filename != "":

            original_filename = secure_filename(attachment.filename)

            extension = os.path.splitext(original_filename)[1]

            filename = f"{uuid.uuid4()}{extension}"

            attachment.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        sender = User.query.filter_by(
            username=session["username"]
        ).first()

        new_letter = Letter(
            sender_id=sender.id,
            receiver_id=int(receiver_id),
            subject=subject,
            body=body,
            attachment=filename
        )

        db.session.add(new_letter)
        db.session.commit()

        flash("Letter sent successfully.", "success")

        return redirect(url_for("main.inbox"))

    return render_template(
        "compose.html",
        users=users
    )


@main.route("/letter/<int:letter_id>")
def view_letter(letter_id):

    if "username" not in session:
        return redirect(url_for("main.login"))

    current_user = User.query.filter_by(
        username=session["username"]
    ).first()

    letter = Letter.query.filter_by(
        id=letter_id,
        receiver_id=current_user.id
    ).first()

    if letter is None:
        flash("Letter not found.", "danger")
        return redirect(url_for("main.inbox"))

    return render_template(
        "view_letter.html",
        letter=letter
    )


@main.route("/download/<filename>")
def download_file(filename):

    if "username" not in session:
        return redirect(url_for("main.login"))

    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=True
    )


@main.route("/logout")
def logout():

    session.clear()

    flash("You have successfully logged out.", "success")

    return redirect(url_for("main.login"))