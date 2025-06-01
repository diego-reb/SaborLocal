from extension import db

class Administrador(db.Model):
    __tablename__='administrador'
    id_administrador = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(80), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)  
    activo= db.Column(db.Boolean, default=True)
    
    
    
    def __repr__(self):
        return f'<Administrador {self.nombre} '