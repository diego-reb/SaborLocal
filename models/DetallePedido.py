from extension import db
  
class DetallePedido(db.Model):
    __tablename__ = 'productopedido'  # Asegúrate de usar el nombre real de la tabla

    id = db.Column(db.Integer, primary_key=True)
    id_pago = db.Column(db.Integer, db.ForeignKey('pago.id_pago', ondelete='CASCADE'), nullable=False)
    nombre_producto = db.Column(db.String(255), nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    # Relación con Pago
    pago = db.relationship('Pago', backref=db.backref('detalles', cascade='all, delete-orphan'))
