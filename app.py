from flask import Flask, render_template, request, redirect
from db import Database
from api import NLPApi

app = Flask(__name__)
dbo = Database()
api = NLPApi()


@app.route('/')
def index():
    return render_template('landing.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/perform_registration', methods=['POST'])
def performed_registration():
    name = request.form.get('user_name')
    email = request.form.get('user_mail')
    password = request.form.get('user_pass')
    response = dbo.insert(name, email, password)
    if response:
        return render_template('login.html', message="Registration Successful. Kindly login to proceed!")
    else:
        return render_template("register.html", message="Email already exists")


@app.route('/perform_login', methods=['POST'])
def performed_login():
    email = request.form.get('user_mail')
    password = request.form.get('user_pass')
    response = dbo.search(email, password)
    if response:
        return redirect("/profile")
    else:
        return render_template('login.html', message="Wrong Email/Password")


@app.route('/profile')
def profile():
    return render_template("profile.html")


# ── NER ──────────────────────────────────────────────────────────────────
@app.route('/ner')
def ner():
    return render_template("ner.html")

@app.route('/perform_ner', methods=['POST'])
def perform_ner():
    text = request.form.get('ner_text')
    search_term = request.form.get('search_term')
    if not text:
        return render_template('ner.html', message="Please enter some text.")
    result = api.ner(text, search_term)
    if not result["ok"]:
        return render_template('ner.html', text=text, message=result["error"])
    ner_data = result["data"]
    entity_count = len(ner_data) if isinstance(ner_data, list) else 0
    return render_template('ner.html', text=text, message=f"NER processed successfully. Entities found: {entity_count}", api_result=ner_data)


# ── Sentiment ─────────────────────────────────────────────────────────────
@app.route('/sentiment', methods=['GET', 'POST'])
def sentiment():
    if request.method == 'POST':
        text = request.form.get('sentiment_text')
        if not text:
            return render_template('sentiment.html', message="Please enter some text.")
        result = api.sentiment_analysis(text)
        if not result["ok"]:
            return render_template('sentiment.html', text=text, message=result["error"])
        return render_template('sentiment.html', text=text, message="Sentiment analysis completed.", api_result=result["data"])
    return render_template('sentiment.html')


# ── Abuse ─────────────────────────────────────────────────────────────────
@app.route('/abuse', methods=['GET', 'POST'])
def abuse():
    if request.method == 'POST':
        text = request.form.get('abuse_text')
        if not text:
            return render_template('abuse.html', message="Please enter some text.")
        result = api.abuse_detection(text)
        if not result["ok"]:
            return render_template('abuse.html', text=text, message=result["error"])
        return render_template('abuse.html', text=text, message="Abuse detection completed.", api_result=result["data"])
    return render_template('abuse.html')


# ── Summarization ─────────────────────────────────────────────────────────
@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    if request.method == 'POST':
        text = request.form.get('summarize_text')
        if not text:
            return render_template('summarize.html', message="Please enter some text.")
        result = api.summarize(text)
        if not result["ok"]:
            return render_template('summarize.html', text=text, message=result["error"])
        return render_template('summarize.html', text=text, message="Summarization completed.", api_result=result["data"])
    return render_template('summarize.html')


# ── Language Detection ────────────────────────────────────────────────────
@app.route('/langdetect', methods=['GET', 'POST'])
def langdetect():
    if request.method == 'POST':
        text = request.form.get('lang_text')
        if not text:
            return render_template('langdetect.html', message="Please enter some text.")
        result = api.detect_language(text)
        if not result["ok"]:
            return render_template('langdetect.html', text=text, message=result["error"])
        return render_template('langdetect.html', text=text, message="Language detected successfully.", api_result=result["data"])
    return render_template('langdetect.html')


# ── Translation ───────────────────────────────────────────────────────────
@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        text = request.form.get('translate_text')
        target = request.form.get('target_language', 'English')
        if not text:
            return render_template('translate.html', message="Please enter some text.")
        result = api.translate(text, target)
        if not result["ok"]:
            return render_template('translate.html', text=text, message=result["error"])
        return render_template('translate.html', text=text, message="Translation completed.", api_result=result["data"])
    return render_template('translate.html')


# ── Spam Detection ────────────────────────────────────────────────────────
@app.route('/spam', methods=['GET', 'POST'])
def spam():
    if request.method == 'POST':
        text = request.form.get('spam_text')
        if not text:
            return render_template('spam.html', message="Please enter some text.")
        result = api.spam_detection(text)
        if not result["ok"]:
            return render_template('spam.html', text=text, message=result["error"])
        return render_template('spam.html', text=text, message="Spam detection completed.", api_result=result["data"])
    return render_template('spam.html')


# ── Grammar Correction ────────────────────────────────────────────────────
@app.route('/grammar', methods=['GET', 'POST'])
def grammar():
    if request.method == 'POST':
        text = request.form.get('grammar_text')
        if not text:
            return render_template('grammar.html', message="Please enter some text.")
        result = api.grammar_correction(text)
        if not result["ok"]:
            return render_template('grammar.html', text=text, message=result["error"])
        return render_template('grammar.html', text=text, message="Grammar correction completed.", api_result=result["data"])
    return render_template('grammar.html')


# ── Keyword Extraction ────────────────────────────────────────────────────
@app.route('/keywords', methods=['GET', 'POST'])
def keywords():
    if request.method == 'POST':
        text = request.form.get('keywords_text')
        if not text:
            return render_template('keywords.html', message="Please enter some text.")
        result = api.keyword_extraction(text)
        if not result["ok"]:
            return render_template('keywords.html', text=text, message=result["error"])
        return render_template('keywords.html', text=text, message="Keywords extracted successfully.", api_result=result["data"])
    return render_template('keywords.html')


if __name__ == '__main__':
    app.run(debug=True)
