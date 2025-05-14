from flask import Flask, render_template
from backend import connectdb

app = Flask(__name__)

@app.route('/udvalg_1')
def udvalg():
  conn = connectdb()
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM produkter")
  produkter = cursor.fetchall()
  
  conn.close()
  
  return render_template('udvalg_1.html', produkter = produkter, tilstand = 'Tændt')
  
