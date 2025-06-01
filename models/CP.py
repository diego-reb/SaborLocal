from extension import db

class CodigoPostal(db.Model):
    __tablename__ = 'codigopostal'
    id_cp = db.Column(db.String(10), primary_key=True)  # Asegúrate de que este campo se llama 'id_cp'
    # Otros campos si los tienes

