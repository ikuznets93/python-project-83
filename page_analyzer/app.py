import os
import psycopg2

from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    )

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


conn = psycopg2.connect(app.config['DATABASE_URL'])
#repo = UserRepository(conn)


@app.route("/")
def index():
    return render_template("index.html")