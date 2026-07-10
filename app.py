from flask import Flask

from backend.database import db
from backend.models import User, Letter

app = Flask(__name__)

# تنظیمات دیتابیس
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mail.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# اتصال دیتابیس به Flask
db.init_app(app)

# ساخت دیتابیس و جدول‌ها
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "<h1>Mail Project is Running ✅</h1>"

if __name__ == "__main__":
    app.run(debug=True)