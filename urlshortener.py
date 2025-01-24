from flask import Flask, request, redirect, render_template, url_for
import random
import string

app = Flask(__name__)

# Store shortened URLs and their original URLs (use a database for production)
url_mapping = {}

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
    url_mapping[short_url] = long_url
    return f"Short URL: <a href='/{short_url}'>/{short_url}</a>"

@app.route('/<short_url>')
def redirect_to_url(short_url):
    long_url = url_mapping.get(short_url)
    if long_url:
        return redirect(long_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
