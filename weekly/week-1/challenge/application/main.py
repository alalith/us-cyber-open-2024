from flask import Flask
from application.blueprints import web, api
from application.util import response
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__,static_url_path="/assets",static_folder="/app/assets")
app.config.from_object('application.config.Config')

app.register_blueprint(web.web, url_prefix='/')
app.register_blueprint(api.api, url_prefix='/api')

@app.errorhandler(404)
def not_found(error):
    return response('404 Not Found'), 404

@app.errorhandler(403)
def forbidden(error):
    return response('403 Forbidden'), 403

@app.errorhandler(400)
def bad_request(error):
    return response('400 Bad Request'), 400

        
        
    



