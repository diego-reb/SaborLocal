from extension import db

class Vendedor(db.Model):
    __tablename__ = 'vendedor'
    
    vendedor_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(80), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)  
    telefono = db.Column(db.String(20))
    activo = db.Column(db.Boolean, default=True)  
    
    
    def __repr__(self):
        return f'<Vendedor {self.nombre} >'