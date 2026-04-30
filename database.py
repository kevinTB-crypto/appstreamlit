import sqlite3

def conectar():
    return sqlite3.connect("panaderia.db", check_same_thread=False)

def crear_tablas():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        total REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS detalle_venta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venta_id INTEGER,
        producto TEXT,
        cantidad INTEGER,
        precio REAL
    )
    """)

    conn.commit()
    conn.close()

def guardar_venta(fecha, total, carrito):
    conn = conectar()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO ventas (fecha, total) VALUES (?, ?)",
        (fecha, total)
    )

    venta_id = cur.lastrowid

    for item in carrito:
        cur.execute("""
        INSERT INTO detalle_venta
        (venta_id, producto, cantidad, precio)
        VALUES (?, ?, ?, ?)
        """, (
            venta_id,
            item["nombre"],
            item["cantidad"],
            item["precio"]
        ))

    conn.commit()
    conn.close()