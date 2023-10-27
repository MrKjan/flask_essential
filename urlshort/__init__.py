from flask import Flask, Blueprint

def create_app(test_confog=None):
    app = Flask(__name__)
    app.secret_key = 'pappa_quokka_secret_key'

    from . import urlshort
    app.register_blueprint(urlshort.bp)

    return app