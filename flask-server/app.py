# flask-server/app.py
import os
from flask import Flask, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(
    __name__,
    template_folder='templates', # HTML files
    static_folder='static'       # CSS, JS, images
)
CORS(app) # Enable CORS for API routes if needed (e.g., during local development with different ports)

# Database Configuration
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Shoe Model
class Shoe(db.Model):
    __tablename__ = 'shoes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    s3link = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Shoe {self.name} (Size: {self.size})>"

    def to_dict(self):
        # Converts a Shoe object to a dictionary for JSON serialization
        return {
            'id': self.id,
            'name': self.name,
            'size': self.size,
            's3link': self.s3link
        }

# Function to create dummy data if the table is empty
def create_dummy_data():
    """
    Populates the 'shoes' table with dummy data if it's currently empty.
    """
    first_image = 'https://gbcproject-frontend.s3.us-east-1.amazonaws.com/10388592_11.webp'
    second_image = 'https://gbcproject-frontend.s3.us-east-1.amazonaws.com/C04288s10.webp'
    if Shoe.query.count() == 0:
        print("Populating database with dummy data...")
        dummy_shoes = [
            Shoe(name='Nike Air Max 270', size=9, s3link=first_image),
            Shoe(name='Adidas Ultraboost 22', size=10, s3link=second_image),
            Shoe(name='Puma RS-X', size=8, s3link=first_image),
            Shoe(name='New Balance 990v5', size=9, s3link=second_image),
            Shoe(name='Converse Chuck Taylor', size=7, s3link=first_image),
            Shoe(name='Vans Old Skool', size=11, s3link=second_image),
            Shoe(name='Reebok Classic', size=8, s3link=first_image),
            Shoe(name='Asics Gel-Kayano', size=10, s3link=second_image),
        ]
        db.session.add_all(dummy_shoes)
        db.session.commit()
        print("Dummy data added successfully!")
    else:
        print("Database already contains data. Skipping dummy data creation.")

# API Route to get all shoes
@app.route('/api/shoes', methods=['GET'])
def get_all_shoes():
    """
    Fetches all shoes from the database and returns them as a JSON array.
    """
    try:
        shoes = Shoe.query.all()
        shoes_data = [shoe.to_dict() for shoe in shoes]
        return jsonify(shoes_data), 200
    except Exception as e:
        app.logger.error(f"Error fetching shoes: {e}")
        return jsonify({"error": "Failed to retrieve shoes", "message": str(e)}), 500

# Route to serve the main HTML page
@app.route('/')
def index():
    """
    Renders the main index.html page.
    """
    return render_template('index.html')

# Main entry point for running the Flask app
if __name__ == '__main__':
    with app.app_context():
        print("Attempting to create database tables...")
        db.create_all() # This will create tables based on models if they don't exist
        print("Database tables checked/created.")
        create_dummy_data() # Populate with dummy data if empty

    # Explicitly set debug and port for local development convenience
    app.run(debug=True, port=5000)
