from extension import db

class TipoUsuario(db.Model):
    __tablename__ = 'tipousuario'
    
    id_ti = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    
    def __init__(self, nombre):
        self.nombre = nombre