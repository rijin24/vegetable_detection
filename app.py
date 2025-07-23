from flask import session
from models import db
from __init__ import create_app

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
