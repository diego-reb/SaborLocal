# models/Colonia.py
from extension import db

class Colonia(db.Model):
    __tablename__ = 'colonia'
    id_col = db.Column(db.Integer, primary_key=True)
    colonia = db.Column(db.String(100), nullable=False)

