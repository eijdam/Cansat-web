from flask import Flask, render_template, request, redirect, url_for, session
import re
import os
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")  # Better to use env var

# Load environment variables
load_dotenv()

# Mail configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = "zochovaspaceagency@gmail.com"
mail = Mail(app)

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

# Database configuration - using PostgreSQL for production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tmp/articles.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
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
    try:
        article = Article.query.get_or_404(article_id)
        return render_template("article.html", article=article)
    except Exception as e:
        print(f"Error fetching article: {str(e)}")
        return "Article not found", 404

@app.route("/")
def home():
    try:
        articles = Article.query.all()
        return render_template("index.html", articles=articles)
    except Exception as e:
        print(f"Error fetching articles: {str(e)}")
        return render_template("index.html", articles=[])

@app.route("/kontakty")
def kontakty():
    message = session.pop("message", None)
    return render_template("kontakt.html", message=message)

@app.route("/tim")
def tim():
    return render_template("tim.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    try:
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message_text = request.form.get("message", "").strip()

        if not all([name, email, message_text]):
            session["message"] = "Všetky polia sú povinné."
            return redirect(url_for("kontakty"))

        if len(message_text) < 10:
            session["message"] = "Správa musí mať aspoň 10 znakov."
            return redirect(url_for("kontakty"))

        if not re.match(EMAIL_REGEX, email):
            session["message"] = "Neplatný email."
            return redirect(url_for("kontakty"))

        msg = Message("Nová správa z kontaktného formulára",
                     recipients=["zochovaspaceagency@gmail.com"])
        msg.body = f"Meno: {name}\nEmail: {email}\nSpráva:\n{message_text}"
        mail.send(msg)
        
        session["message"] = "Správa bola úspešne odoslaná."
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        session["message"] = "Nastala chyba pri odosielaní správy."
    
    return redirect(url_for("kontakty"))

# For local development
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8080)