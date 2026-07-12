from flask import Flask
import os

from werkzeug.security import generate_password_hash

from backend.database import db
from backend.models import User
from backend.routes import main

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

# مسیر پوشه uploads
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# حداکثر حجم فایل (16MB)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

# تنظیمات برنامه
app.config["SECRET_KEY"] = "mail_project_secret_key"

# اتصال به دیتابیس
# اگر داخل Docker اجرا شود از متغیر محیطی استفاده می‌کند،
# در غیر این صورت از localhost استفاده خواهد کرد.
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "SQLALCHEMY_DATABASE_URI",
    "postgresql+psycopg2://mailuser:mailpass@localhost:5432/maildb"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# اتصال SQLAlchemy
db.init_app(app)

# ساخت جدول‌ها و کاربران اولیه
with app.app_context():

    db.create_all()

    if User.query.count() == 0:

        admin = User(
            username="admin",
            password=generate_password_hash("1234")
        )

        amir = User(
            username="amir",
            password=generate_password_hash("1234")
        )

        db.session.add(admin)
        db.session.add(amir)
        db.session.commit()

# ثبت Routeها
app.register_blueprint(main)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )