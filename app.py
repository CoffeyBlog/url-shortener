from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'frog'  # make secret key very difficult for production


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        # if the url entered by the user is already in the .json file ... return the user to home
        if request.form['code'] in urls.keys():
            flash(
                'That short name has already been taken, please select another name')  # if the url entered by the user is already in the .json file ... flash an h2 tag via jinja that says URL has been taken
            return redirect(url_for('home'))

        # Goes through form to see if there is something called url
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']  # is short for file
            full_name = request.form['code'] + secure_filename(
                f.filename)  # wekzeug is a security library created by the flask team
            f.save('/Users/lucascoffey/Desktop/url-shortener/static/user_files' + full_name)
            urls[request.form['code']] = {'file': full_name}

        # put the url that the user entered in the request form and save it to the .json file
        urls[request.form['code']] = {'url': request.form['url']}  # code = shortcode & url is the codes url
        with open('urls.json', 'w') as url_file:  # open the urls.json file and write as url
            json.dump(urls, url_file)
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))


@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'urls' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))


if __name__ == "__main__":
    app.run()
