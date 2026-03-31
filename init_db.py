import sqlite3

conn = sqlite3.connect('bolao.db')

conn.execute("""
CREATE TABLE IF NOT EXISTS jogos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time1 TEXT,
    time2 TEXT,
    real_g1 INTEGER,
    real_g2 INTEGER
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS apostas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jogo_id INTEGER,
    nome TEXT,
    g1 INTEGER,
    g2 INTEGER,
    pontos INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()
