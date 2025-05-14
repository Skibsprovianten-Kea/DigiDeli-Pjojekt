from flask import Flask, render_template
from backend import connectdb

app = Flask(__name__)

@app.route('/udvalg')
def udvalg():
  conn = connectdb()
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM produkter")
  produkter = cursor.fetchall()
  
  conn.close()
  
  return render_template('udvalg.html', produkter = produkter, tilstand = 'Tændt')
  
