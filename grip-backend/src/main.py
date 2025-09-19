import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file in the backend directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.commodity import commodity_bp
from src.routes.country import country_bp
from src.routes.data import data_bp
from src.routes.collection import collection_bp
from src.routes.analytics import analytics_bp
from src.routes.api_keys import api_keys_bp
from src.routes.fred_test import fred_test_bp
from src.routes.usgs_test import usgs_test_bp
from src.routes.file_ingestion import file_ingestion_bp

# Import all models to ensure they are registered with SQLAlchemy
from src.models.commodity import Commodity
from src.models.country import Country
from src.models.production_data import ProductionData
from src.models.reserves_data import ReservesData
from src.models.price_data import PriceData
from src.models.data_source import DataSource
from src.models.api_key import APIKey

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')

# Enable CORS for all routes
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(commodity_bp, url_prefix='/api')
app.register_blueprint(country_bp, url_prefix='/api')
app.register_blueprint(data_bp, url_prefix='/api')
app.register_blueprint(collection_bp, url_prefix='/api')
app.register_blueprint(analytics_bp, url_prefix='/api')
app.register_blueprint(api_keys_bp)
app.register_blueprint(fred_test_bp)
app.register_blueprint(usgs_test_bp)
app.register_blueprint(file_ingestion_bp)

# Database configuration from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
