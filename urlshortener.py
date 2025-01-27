from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(6), unique=True, nullable=False)
    click_count = db.Column(db.Integer, default=0)  # Track the number of clicks

with app.app_context(): 
    db.create_all()  # Creates the database and tables

def generate_short_url():
    """Generate a random string of 6 characters"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    short_url = generate_short_url()

    # Check if the short URL already exists (in case of collisions)
    while URLMapping.query.filter_by(short_url=short_url).first():
        short_url = generate_short_url()

    # Save the mapping in the database
    new_url = URLMapping(long_url=long_url, short_url=short_url)
    db.session.add(new_url)
    db.session.commit()

    return render_template('index.html', short_url=short_url)

@app.route('/<short_url>')
def redirect_to_url(short_url):
    url_mapping = URLMapping.query.filter_by(short_url=short_url).first()
    if url_mapping:
        url_mapping.click_count += 1
        db.session.commit()
        return redirect(url_mapping.long_url)
    return "URL not found", 404

@app.route('/details/<short_url>')
def show_details(short_url):
    """Page to show details for the shortened URL."""
    url_mapping = URLMapping.query.filter_by(short_url=short_url).first()
    if url_mapping:
        return render_template('details.html', url_mapping=url_mapping)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
