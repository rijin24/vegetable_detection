from . import db
import uuid

class Store(db.Model):
    __tablename__ = 'store'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, unique=True)
    postcode = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean, default=True)
