import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
metadata = db.metadata

ma = Marshmallow()
cache = Cache()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    
    db_parameters = {
        "user": os.getenv('DB_USER'),
        "password": os.getenv('DB_PASSWORD'),
        "host": os.getenv('DB_HOST', 'localhost'),
        "port": os.getenv('DB_PORT', '3306'),
        "dbname": os.getenv('DB_NAME')
    }

    ma.init_app(app)
    cache.init_app(app, config={
        'CACHE_TYPE': 'RedisCache',
        'CACHE_DEFAULT_TIMEOUT': 300,
        'CACHE_REDIS_HOST': os.getenv('REDIS_HOST'),
        'CACHE_REDIS_PORT': os.getenv('REDIS_PORT'),
        'CACHE_REDIS_DB': os.getenv('REDIS_DB'),
        'CACHE_REDIS_PASSWORD': os.getenv('REDIS_PASSWORD'),
        'CACHE_KEY_PREFIX': 'user_'
    })

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_RECORD_QUERIES'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_parameters['user']}:{db_parameters['password']}@{db_parameters['host']}:{db_parameters['port']}/{db_parameters['dbname']}"
    
    db.init_app(app)
    
    migrate = Migrate(app, db)

    from app.resources.reserve import reserve
    app.register_blueprint(reserve, url_prefix='/api/v1/')

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
