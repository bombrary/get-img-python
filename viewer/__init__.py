from flask import Flask, render_template, request
from getimg import get_img_urls

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        url = request.form['url']
        selector = request.form['selector']

        if url is not None:
            urls = get_img_urls(url, selector)
            return render_template('index.html', urls = urls)

    return render_template('index.html')
