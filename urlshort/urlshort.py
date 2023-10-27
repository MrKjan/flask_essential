from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
    session,
    jsonify,
)
import json
import os.path
from werkzeug.utils import secure_filename

bp = Blueprint('urlshort', __name__)

@bp.route('/')
def home():
    print(f'{session.keys=}')
    return render_template('home.html', codes=session.keys())


@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('static/shortcodes/urls.json'):
        with open('urlshort/static/shortcodes/urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:  # 'file'
                    file_url = url_for(
                        'static', filename='file_storage/' + urls[code]['file'])
                    print(f'{file_url=}')
                    return redirect(file_url)
    return abort(404)


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@bp.route('/your-url/', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        if os.path.exists('urlshort/static/shortcodes/urls.json'):
            with open('urlshort/static/shortcodes/urls.json') as urls_file:
                urls = json.load(urls_file)
        else:
            urls = {}

        if request.form['code'] in urls.keys():
            flash(f'Name {request.form["code"]} is already used!')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:  # 'file'
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('C:/wrk/flasklearn/flask_essential/urlshort/static/file_storage/' + full_name)
            urls[request.form['code']] = {'file': full_name}

        with open('urlshort/static/shortcodes/urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home'))


@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
