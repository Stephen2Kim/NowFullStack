from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db
from flask_cors import CORS
import json
from datetime import time, datetime

# Custom JSON Encoder to handle time and datetime objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, time):
            return obj.strftime('%H:%M')  # Convert time to string (HH:MM format)
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO format (YYYY-MM-DDTHH:MM:SS)
        return super().default(obj)

app = Flask(__name__)
CORS(app)

# Set the secret key for session management
app.secret_key = 'your_secret_key_here'

# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Set the custom JSON encoder
app.json_encoder = CustomJSONEncoder

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Import routes after app initialization
from routes import *

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
