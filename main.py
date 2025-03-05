from flask import Flask, render_template, request, redirect, url_for, session
import re
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Initialize the Flask app
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

# Static articles (list of dictionaries)
articles = [
    {"id": 1, "title": "O nás", "content": "Predstavenie tímu a nášho projektu"},
    {"id": 2, "title": "Náš progres", "content": "Náš pokrok do 9.3. "},
    {"id": 3, "title": "Pripravujeme", "content": "Tento článok bude zverejnený čoskoro"}
]

# Routes
@app.route("/")
def home():
    return render_template("index.html", articles=articles)

@app.route("/clanky/<int:article_id>")
def article(article_id):
    # Find article by ID
    article = next((a for a in articles if a["id"] == article_id), None)
    if article:
        # For article 2, render a different template
        if article_id == 2:
            return render_template("article2.html", article=article)
        else:
            return render_template("article.html", article=article)
    else:
        return "Article not found", 404

@app.route("/kontakty")
def kontakty():
    message = session.pop("message", None)
    return render_template("kontakt.html", message=message)

@app.route("/blog")
def blog():
    return render_template("blog.html", articles=articles)


@app.route("/tim")
def tim():
    return render_template("tim.html")

@app.route("/sponsor")
def sponsor():
    return render_template("sponsor.html")

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

if __name__ == "__main__":
    app.run(debug=True)
