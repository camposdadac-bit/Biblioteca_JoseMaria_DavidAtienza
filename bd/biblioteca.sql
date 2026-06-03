BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS libros (
    id INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    isbn TEXT,
    disponible INTEGER NOT NULL DEFAULT 1,
    categoria TEXT DEFAULT 'General',
    fecha_actualizacion TEXT
);

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    email TEXT NOT NULL,
    habilitado BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS prestamos (
    id_prestamo INTEGER PRIMARY KEY AUTOINCREMENT,
    libro_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    fecha_prestamo TEXT NOT NULL DEFAULT (DATE('now')),
    fecha_devolucion TEXT,
    estado TEXT NOT NULL DEFAULT 'prestado',
    FOREIGN KEY (libro_id) REFERENCES libros(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS biblioteca (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre TEXT
);
COMMIT;