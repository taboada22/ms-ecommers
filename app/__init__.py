import os
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_caching import Cache
from app.Config import config
from app.Config.cache_config import cache_config
from flask_cors import CORS

ma = Marshmallow()
cache = Cache()

def create_app() -> Flask:
    
    app_context = os.getenv('FLASK_CONTEXT')
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)
    ma.init_app(app)
    cache.init_app(app, config=cache_config)
    CORS(app)

    from app.Routes.builder import builder
    app.register_blueprint(builder)
    
    @app.shell_context_processor    
    def ctx():
        return {"app": app}
    
    return app
