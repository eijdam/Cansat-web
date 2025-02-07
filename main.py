from flask import Flask, render_template, request, redirect, url_for, session
import re
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Flask-Mail Configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "zochovaspaceagency@gmail.com"
app.config["MAIL_PASSWORD"] = "wqdq edek wqhe uahl"
app.config["MAIL_DEFAULT_SENDER"] = "zochovaspaceagency@gmail.com"

mail = Mail(app)

# Email validation regex
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

# Set up the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)

# Define the Article model (database table)
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Article {self.title}>"

# Route to display a single article
@app.route("/clanky/<int:article_id>")
def article(article_id):
    article = Article.query.get_or_404(article_id)  # Fetch article by ID, or 404 if not found
    return render_template("article.html", article=article)

@app.route("/")
def home():
    articles = Article.query.all()  # Fetch all articles
    return render_template("index.html", articles=articles)

@app.route("/kontakty")
def kontakty():
    message = session.pop("message", None)  # Retrieve and clear the message
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

# Add this at the end of main.py
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the tables
    app.run(debug=True)
