import sqlite3

DB = "controle_uber.db"

def connect():
    """Retorna uma conexão SQLite inicializada com as tabelas necessárias."""
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS corridas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        valor REAL NOT NULL,
        km REAL NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS abastecimentos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        litros REAL NOT NULL,
        preco_l REAL NOT NULL
    )
    """)
    conn.commit()
    return conn
