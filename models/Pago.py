from extension import db
class Pago(db.Model):
    __tablename__ = "pago"
    id_pago = db.Column(db.Integer, primary_key=True)

    # Dirección
    direccion = db.Column(db.String(255), nullable=False)
    colonia = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.String(10), nullable=False)

    # Entrega
    horario_entrega = db.Column(db.String(50), nullable=True)
    notas_adicionales = db.Column(db.String(255), nullable=True)
    fecha_entrega = db.Column(db.String(50), nullable=False)

    # Datos personales
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)

    # Método de pago
    metodo_pago = db.Column(db.String(50), nullable=False)

    # Información de tarjeta (solo si el método de pago es tarjeta)
    numero_tarjeta = db.Column(db.String(16), nullable=True)
    cvv = db.Column(db.String(4), nullable=True)
    fecha_expiracion = db.Column(db.String(7), nullable=True)

    def __repr__(self):
        return f"<Pago {self.id_pago}, {self.nombre}, {self.metodo_pago}>"
