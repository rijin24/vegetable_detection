from flask import Flask
from models import db
from admin.routes import admin_bp
from store.routes import store_bp
from mobile.routes import mobile_bp


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)

    app.register_blueprint(admin_bp)
    app.register_blueprint(store_bp)
    app.register_blueprint(mobile_bp)

    return app
