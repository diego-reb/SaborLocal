from extension import db

class Direccion(db.Model):
    __tablename__ = 'direccion'
    id_di = db.Column(db.Integer, primary_key=True)
    calle = db.Column(db.String(200))
    id_col = db.Column(db.String(10), db.ForeignKey('colonia.id_col'), nullable=False)  # Clave foránea para colonia
    id_al = db.Column(db.String(10), db.ForeignKey('alcaldia.id_al'), nullable=False)
    lote = db.Column(db.String(50))
    mz = db.Column(db.String(50))
    id_cp = db.Column(db.String(10), db.ForeignKey('codigopostal.id_cp'))

    numero = db.Column(db.String(20))
    num_ext = db.Column(db.String(20))
    referencias = db.Column(db.String(300))

    colonia = db.relationship('Colonia', backref=db.backref('direcciones', lazy=True))
    alcaldia = db.relationship('Alcaldia', backref=db.backref('direcciones', lazy=True))
    codigo_postal = db.relationship('CodigoPostal', backref=db.backref('direcciones', lazy=True)) 

