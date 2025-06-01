from extension import db

class Alcaldia(db.Model):
    __tablename__ = 'alcaldia'
    id_al = db.Column(db.Integer, primary_key=True)
    alcaldia = db.Column(db.String(100), nullable=False)
