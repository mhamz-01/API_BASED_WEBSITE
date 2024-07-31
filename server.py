from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from config import Config

app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SECRET_KEY'] = 'hamza123'  # Add your secret key here


db = SQLAlchemy(app)
mail = Mail(app)

# Model for storing emails
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Function to get the number of verses in a chapter
def get_verses(chapter, limit):
    url = f"https://al-quran1.p.rapidapi.com/{chapter}/1-{limit}"
    headers = {
        "x-rapidapi-key": "57ff59a728msh25e5d1841f684f6p1e83b3jsn7e6aa0a163f5",
        "x-rapidapi-host": "al-quran1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Function to send daily verses
def send_daily_verse():
    # Fetch a random verse (for simplicity, we are using chapter 1, verse 1)
    verses = get_verses(1, 1)
    verse_info = next(iter(verses.values()))
    verse_content = verse_info['content']
    verse_translation = verse_info['translation_eng']
    verse_transliteration = verse_info['transliteration']

    with app.app_context():
        emails = Email.query.all()
        for email_entry in emails:
            msg = Message("Daily Quran Verse",
                          sender="your_email@example.com",
                          recipients=[email_entry.email])
            msg.body = (f"Verse:\n{verse_content}\n\n"
                        f"Translation:\n{verse_translation}\n\n"
                        f"Transliteration:\n{verse_transliteration}")
            mail.send(msg)

# Schedule daily emails
scheduler = BackgroundScheduler()
scheduler.add_job(func=send_daily_verse, trigger="interval", days=1)
scheduler.start()

@app.route("/", methods=["GET", "POST"])
def home():
    verses = None
    if request.method == "POST":
        if 'chapter' in request.form and 'limit' in request.form:
            chapter = request.form.get("chapter")
            limit = request.form.get("limit")
            verses = get_verses(chapter, limit)
        elif 'email' in request.form:
            email = request.form.get("email")
            if email:
                new_email = Email(email=email)
                try:
                    db.session.add(new_email)
                    db.session.commit()
                    flash("Email added successfully!", "success")
                except:
                    db.session.rollback()
                    flash("Email already exists or invalid!", "danger")
                return redirect(url_for("home"))
    return render_template("index.html", verses=verses)

if __name__ == "__main__":

    app.run(debug=True)
