from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
metadata = db.metadata
migrate = Migrate()

def create_app():
    print(os.getcwd())
    load_dotenv()
    print(os.getenv("DEV_DATABASE_URI"))  # Verifica si se carga correctamente

    config_name = os.getenv("FLASK_ENV")
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DEV_DATABASE_URI")
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.shell_context_processor
    
    def ctx():
        return{"app": app}

    return app
