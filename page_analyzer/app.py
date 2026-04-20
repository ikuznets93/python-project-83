import os
import psycopg2

from dotenv import load_dotenv
from flask import (
    abort,
    get_flashed_messages,
    flash,
    Flask,
    redirect,
    render_template,
    request,
    url_for
)
from page_analyzer.url_repository import UrlRepository
from .url_validator import normalize_url, validate_url

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


conn = psycopg2.connect(app.config['DATABASE_URL'])
repo = UrlRepository(conn)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/urls", methods=["POST"])
def urls_index():
    url = request.form.to_dict()
    errors = validate_url(url["url"])
    if errors:
        flash("Некорректный URL", "danger")
        return render_template(
            "index.html",
        ), 422
    
    normalized_url = normalize_url(url["url"])
    url_info = repo.find_url(normalized_url)
    if url_info is not None:
        flash("Указанный URL уже существует", "warning")
        return redirect(url_for("get_url", id=url_info["id"]))
    
    id = repo.add(normalized_url)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("get_url", id=id))

@app.route("/urls/<int:id>")
def get_url(id):
    url_info = repo.find_id(id)

    if not url_info:
        abort(404)

    return render_template("url.html", url_info=url_info)

@app.route("/urls", methods=["GET"])
def get_urls():
    urls_content = repo.get_content()
    return render_template("urls.html", urls_content=urls_content)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


