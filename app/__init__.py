from flask import Flask
import os
from app.config import config
from flask_marshmallow import Marshmallow
from flask_caching import Cache
from app.config.cache_config import cache_config


ma = Marshmallow()
cache = Cache()

def create_app():
    app_context = os.getenv('FLASK_CONTEXT')
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)
    ma.init_app(app)
    #cache.init_app(app, config=cache_config)

    #from app.resources import purchase
    #app.register_blueprint(purchase)
    from app.resources import purchase
    app.register_blueprint(purchase, url_prefix='/comercio')
    
    @app.shell_context_processor    
    def ctx():
        return {"app": app}
    
    return app