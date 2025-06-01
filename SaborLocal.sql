select * from pago
select * from vendedor
select * from cliente
select * from pedidos
CREATE TABLE pago (
    id_pago SERIAL PRIMARY KEY,
    direccion VARCHAR(255) NOT NULL,
    colonia VARCHAR(100) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    codigo_postal VARCHAR(10) NOT NULL,
    horario_entrega VARCHAR(50),
    notas_adicionales VARCHAR(255),
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    metodo_pago VARCHAR(50) NOT NULL,
    fecha_entrega VARCHAR(50) NOT NULL
);
ALTER TABLE pago ADD COLUMN numero_tarjeta VARCHAR(16);
ALTER TABLE pago ADD COLUMN cvv VARCHAR(4);


UPDATE vendedor
SET contraseña = 'scrypt:32768:8:1$dUM46qKqCSrvtptv$c80960894c614077995d0212cfb195aa47c3a431fc42b954aa6d75f625a1297d8788a1cece97c11a9d4098246f758cfc0aa57e5e05d280efeacc536fb3f3881f'
WHERE correo = 'ale092@gmail.com';

ALTER TABLE producto ADD COLUMN imagen bytea;

select * from producto