from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
CORS(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ucpuppeziwjiat:47f0858773684f79d81960b9c996b775ef00afa618b7b9f4386a6ddd4248c120@ec2-34-247-72-29.eu-west-1.compute.amazonaws.com:5432/d4nua1df080bql"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class URL_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(300), nullable=False, unique=True)
    short_url = db.Column(db.String(8), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, url, short_url):
        self.url = url
        self.short_url = short_url

    def __repr__(self):
        return f"<Original URL: '{self.url}'>, Short URL: '{self.short_url}'>"


def generate_short_url():
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    while True:
        random_letters = random.choices(letters, k=8)
        random_string = "".join(random_letters)
        url_is_duplicate = URL_Data.query.filter_by(short_url=random_string).first()
        if not url_is_duplicate:
            return random_string


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if request.form:
            submitted_url = request.form["url"]
        else:
            data = request.get_json()
            submitted_url = data["url"]
        url_in_db = URL_Data.query.filter_by(url=submitted_url).first()
        if url_in_db:
            full_short_url = f"http://127.0.0.1:5000/{url_in_db.short_url}"
            if request.form: 
                return render_template("home.html", submitted_url=submitted_url, full_short_url=full_short_url, button_text="Shorten another URL"   )
            else:                
                return f"<h2><a href={submitted_url} target='_blank'>{submitted_url}</a></h2>     <h3>Short URL: <a href={full_short_url} target='_blank'>{full_short_url}</a></h3>"

        else:
            try:
                shorten_url = generate_short_url()
                new_url = URL_Data(url=submitted_url, short_url=shorten_url)
                db.session.add(new_url)
                db.session.commit()
                full_new_short_url = f"http://127.0.0.1:5000/{shorten_url}"
                
                if request.form:     
                    return render_template("home.html", submitted_url=submitted_url, full_short_url=full_new_short_url, button_text="Shorten another URL"  )
                else:
                    return f"<h2><a href={submitted_url} target='_blank'>{submitted_url}</a></h2> <h3>Short URL: <a href={full_new_short_url} target='_blank'>{full_new_short_url}</a></h3>"

            except:
                return "There was an issue adding the url"
    else:
        return render_template("home.html", submitted_url="", full_short_url="", button_text="Shorten URL" )


@app.route("/all_urls", methods=["GET"])
def index():
    urls = URL_Data.query.order_by(URL_Data.date_created).all()
    return render_template("all_urls..html", urls=urls)


@app.route("/<string:s_url>")
def redirect_to_url(s_url):
    url_in_db = URL_Data.query.filter_by(short_url=s_url).first()
    if url_in_db:
        return redirect(f"{url_in_db.url}")
    else:
        return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    url_to_delete = URL_Data.query.get_or_404(id)
    try:
        db.session.delete(url_to_delete)
        db.session.commit()
        return redirect("/all_urls")
    except:
        return "There was a problem deleting the URL"


# @app.route("/update/<int:id>", methods=["GET", "POST"])
# def update(id):
#     task_to_update = URL_Data.query.get_or_404(id)
#     if request.method == "POST":
#         task_to_update.content = request.form["content"]
#         try:
#             db.session.commit()
#             return redirect("/")
#         except:
#             return "There was an issue updateing your task"
#     else:
#         return render_template("update.html", task=task_to_update)


if __name__ == "__main__":
    app.run()
