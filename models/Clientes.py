from extension import db

class TipoUsuario(db.Model):
    __tablename__ = 'tipo_usuario'
    id_ti = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))  # 'cliente', 'vendedor', 'admin'
    permisos = db.Column(db.String(200)) 

class Clientes(db.Model):
    __tablename__ = 'cliente'
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    contraseña = db.Column(db.String(300))
    telefono = db.Column(db.String(20))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
    ti_id = db.Column(db.Integer, db.ForeignKey('tipousuario.id_ti'))  # Revisa si 'tipos' es el nombre correcto
    activo = db.Column(db.Boolean, default=True)  
