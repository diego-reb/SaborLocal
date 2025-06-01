from extension import db

class ProductoPedido(db.Model):
    _tablename_ = 'producto_pedido'

    id = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String(100), nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    id_pago = db.Column(db.Integer, db.ForeignKey('pago.id_pago'), nullable=False)
    pago = db.relationship('Pago', backref=db.backref('productos', lazy=True))