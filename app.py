from flask import Flask
from werkzeug.security import generate_password_hash

from backend.database import db
from backend.models import User, Letter
from backend.routes import main

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

# تنظیمات برنامه
app.config["SECRET_KEY"] = "mail_project_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mail.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# اتصال دیتابیس
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
    app.run(debug=True)