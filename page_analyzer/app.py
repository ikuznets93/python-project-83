import os

import psycopg2
import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.html_parser import parser
from page_analyzer.url_repository import UrlRepository
from page_analyzer.url_validator import normalize_url, validate_url

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
        flash("Страница уже существует", "warning")
        return redirect(url_for("get_url", id=url_info["id"]))
    
    id = repo.add_url(normalized_url)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("get_url", id=id))


@app.route("/urls/<int:id>")
def get_url(id):
    url_info = repo.find_id(id)

    if not url_info:
        abort(404)

    checks_data = repo.get_url_checks(id)
    return render_template(
        "url.html", 
        url_info=url_info, 
        checks_data=checks_data
    )


@app.route("/urls", methods=["GET"])
def get_urls():
    urls_content = repo.get_urls_last_checks()
    return render_template("urls.html", urls_content=urls_content)


@app.route("/urls/<int:id>/checks", methods=["POST"])
def add_url_check(id):
    url_info = repo.find_id(id)
    
    try:
        response = requests.get(url_info.get("name"), timeout=0.5)
        response.raise_for_status()
    except requests.RequestException:
        flash("Произошла ошибка при проверке", "danger")
        return redirect(url_for("get_url", id=id))
    
    status_code = response.status_code
    page_data = parser(response)
    page_data["status_code"] = status_code
    repo.add_url_check(url_info, page_data)
    flash("Страница успешно проверена", "success")
    checks_data = repo.get_url_checks(id)
    return render_template(
        "url.html",
        url_info=url_info,
        checks_data=checks_data
    )
    

@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


