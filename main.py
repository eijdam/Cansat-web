from flask import Flask, render_template, request, redirect, url_for, session
import re
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "your_secret_key"


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "zochovaspaceagency@gmail.com"
app.config["MAIL_PASSWORD"] = "wqdq edek wqhe uahl"
app.config["MAIL_DEFAULT_SENDER"] = "zochovaspaceagency@gmail.com"

mail = Mail(app)

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Article {self.title}>"


@app.route("/clanky/<int:article_id>")
def article(article_id):
    article = Article.query.get_or_404(article_id) 
    return render_template("article.html", article=article)

@app.route("/")
def home():
    articles = Article.query.all()  
    return render_template("index.html", articles=articles)

@app.route("/kontakty")
def kontakty():
    message = session.pop("message", None)  
    return render_template("kontakt.html", message=message)

@app.route("/tim")
def tim():
    return render_template("tim.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    name = request.form.get("name").strip()
    email = request.form.get("email").strip()
    message_text = request.form.get("message").strip()

    if not name or not email or not message_text:
        return redirect(url_for("kontakty"))

    if len(message_text) < 10:
        return redirect(url_for("kontakty"))

    try:
        msg = Message("Nová správa z kontaktného formulára",
                      recipients=["zochovaspaceagency@gmail.com"])
        msg.body = f"Meno: {name}\nEmail: {email}\nSpráva:\n{message_text}"
        mail.send(msg)
    except Exception as e:
        print(f"Nastala chyba: {str(e)}")

    return redirect(url_for("kontakty"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
