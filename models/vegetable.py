from . import db
from sqlalchemy import UniqueConstraint

class Vegetable(db.Model):
    __tablename__ = 'vegetable'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_path = db.Column(db.String(200))
    store_id = db.Column(db.String(36), db.ForeignKey('store.id'), nullable=False)

    store = db.relationship('Store', backref=db.backref('vegetables', lazy=True))

    __table_args__ = (
        UniqueConstraint('name', 'store_id', name='uq_vegetable_store'),
    )
