from flask import Flask
from psycopg2 import 
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Working!"

@app.route("/explain")
def explain(query):
    conn = psycopg2.connect(
        host="localhost",
        database="database",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    cur.execute('explain analyze '+query)
    result = cur.fetchall()
    return result
