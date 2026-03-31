from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def conectar():
    return sqlite3.connect('bolao.db')

@app.route('/')
def index():
    conn = conectar()
    jogos = conn.execute("SELECT * FROM jogos").fetchall()
    conn.close()
    return render_template('index.html', jogos=jogos)

@app.route('/apostar/<int:jogo_id>', methods=['GET','POST'])
def apostar(jogo_id):
    conn = conectar()

    if request.method == 'POST':
        nome = request.form['nome']
        g1 = request.form['g1']
        g2 = request.form['g2']

        conn.execute(
            "INSERT INTO apostas (jogo_id, nome, g1, g2) VALUES (?, ?, ?, ?)",
            (jogo_id, nome, g1, g2)
        )
        conn.commit()
        conn.close()
        return redirect('/')

    jogo = conn.execute("SELECT * FROM jogos WHERE id=?", (jogo_id,)).fetchone()
    conn.close()
    return render_template('apostar.html', jogo=jogo)

@app.route('/resultado/<int:jogo_id>', methods=['POST'])
def resultado(jogo_id):
    g1 = int(request.form['g1'])
    g2 = int(request.form['g2'])

    conn = conectar()
    conn.execute("UPDATE jogos SET real_g1=?, real_g2=? WHERE id=?", (g1, g2, jogo_id))

    apostas = conn.execute("SELECT * FROM apostas WHERE jogo_id=?", (jogo_id,)).fetchall()

    for a in apostas:
        pontos = calcular(a[3], a[4], g1, g2)
        conn.execute("UPDATE apostas SET pontos=? WHERE id=?", (pontos, a[0]))

    conn.commit()
    conn.close()
    return redirect('/ranking')

def calcular(p1, p2, r1, r2):
    if p1 == r1 and p2 == r2:
        return 5
    if (p1 > p2 and r1 > r2) or (p1 < p2 and r1 < r2) or (p1 == p2 and r1 == r2):
        return 3
    return 0

@app.route('/ranking')
def ranking():
    conn = conectar()
    ranking = conn.execute("""
        SELECT nome, SUM(pontos) as total
        FROM apostas
        GROUP BY nome
        ORDER BY total DESC
    """).fetchall()
    conn.close()
    return render_template('ranking.html', ranking=ranking)
