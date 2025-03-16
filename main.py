from flask import Flask, render_template, request, redirect, url_for, session
import re
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv
from flask_babel import Babel, get_locale

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")

# Load environment variables
load_dotenv()

# Babel configuration
def get_locale_from_session():
    if 'language' in session:
        return session['language']
    return request.accept_languages.best_match(['sk', 'en'])

babel = Babel(app, locale_selector=get_locale_from_session)
app.config['BABEL_DEFAULT_LOCALE'] = 'sk'
app.config['LANGUAGES'] = ['sk', 'en']

# Mail configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = "zochovaspaceagency@gmail.com"
mail = Mail(app)

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

@app.route('/set_language/<language>')
def set_language(language):
    if language in app.config['LANGUAGES']:
        session['language'] = language
    return redirect(request.referrer or url_for('home'))

# Static articles with translations
articles = [
    {
        "id": 1,
        "title": {"sk": "O nás", "en": "About Us"},
        "content": {"sk": "Predstavenie tímu a nášho projektu. Sme študentský tím zo SPŠE Zochova 9 v Bratislave, ktorý sa zúčastňuje súťaže CanSat. Náš projekt sa zameriava na vývoj miniatúrneho satelitu, ktorý bude zbierať dáta o zalesnení zeme.", 
                   "en": "Introduction of our team and project. We are a student team from SPŠE Zochova 9 High School in Bratislava, participating in the CanSat competition. Our project focuses on developing a miniature satellite that will collect data regarding forest coverage of the Earth."}
    },
    {
        "id": 2,
        "title": {"sk": "Náš progres", "en": "Our Progress"},
        "content": {"sk": "Náš pokrok do 9.3. Počas posledných týždňov sme dosiahli významný pokrok v našom projekte. Dokončili sme základný návrh hardvéru, začali sme s programovaním senzorov a vytvorili sme prvé prototypy našich systémov.", 
                   "en": "Our progress until March 9. Over the past few weeks, we have made significant progress in our project. We completed the basic hardware design, started programming the sensors, and created the first prototypes of our systems."}
    },
    {
        "id": 3,
        "title": {"sk": "Pripravujeme", "en": "Coming Soon"},
        "content": {"sk": "Tento článok bude zverejnený čoskoro. Sledujte náš blog pre najnovšie informácie o našom projekte a pripravovaných aktivitách.", 
                   "en": "This article will be published soon. Follow our blog for the latest information about our project and upcoming activities."}
    }
]

# Routes
@app.route("/")
def home():
    lang = str(get_locale())
    translated_articles = [
        {
            "id": article["id"],
            "title": article["title"][lang],
            "content": article["content"][lang]
        }
        for article in articles
    ]
    return render_template("index.html", articles=translated_articles)

@app.route("/clanky/<int:article_id>")
def article(article_id):
    lang = str(get_locale())
    article = next((a for a in articles if a["id"] == article_id), None)
    if article:
        translated_article = {
            "id": article["id"],
            "title": article["title"][lang],
            "content": article["content"][lang]
        }
        if article_id == 2:
            return render_template("article2.html", article=translated_article)
        else:
            return render_template("article.html", article=translated_article)
    else:
        return "Article not found", 404

@app.route("/kontakty")
def kontakty():
    message = session.pop("message", None)
    return render_template("kontakt.html", message=message)

@app.route("/blog")
def blog():
    lang = str(get_locale())
    translated_articles = [
        {
            "id": article["id"],
            "title": article["title"][lang],
            "content": article["content"][lang]
        }
        for article in articles
    ]
    return render_template("blog.html", articles=translated_articles)

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
            session["message"] = "All fields are required."
            return redirect(url_for("kontakty"))

        if len(message_text) < 10:
            session["message"] = "Message must be at least 10 characters long."
            return redirect(url_for("kontakty"))

        if not re.match(EMAIL_REGEX, email):
            session["message"] = "Invalid email address."
            return redirect(url_for("kontakty"))

        msg = Message("New message from contact form",
                     recipients=["zochovaspaceagency@gmail.com"])
        msg.body = f"Name: {name}\nEmail: {email}\nMessage:\n{message_text}"
        mail.send(msg)
        
        session["message"] = "Message was sent successfully."
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        session["message"] = "An error occurred while sending the message."
    
    return redirect(url_for("kontakty"))

if __name__ == "__main__":
    app.run(debug=True)
