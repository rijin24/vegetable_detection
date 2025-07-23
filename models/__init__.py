from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .store import Store
from .vegetable import Vegetable
