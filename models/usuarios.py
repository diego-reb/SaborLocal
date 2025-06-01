from extension import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    contraseña = db.Column(db.String(250), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)

    def __init__(self, nombre, correo, contraseña, telefono):
        self.nombre = nombre
        self.correo = correo
        self.contraseña = contraseña
        self.telefono = telefono