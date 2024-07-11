from flask import Flask, request, jsonify, session
from flask_cors import CORS
from models import User, db
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from main import searchFlights
import os
import uuid

load_dotenv()

app = Flask(__name__)

# Configure your Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///flaskdb.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')  # Ensure this key is strong and secure

# Enable CORS for requests including credentials
CORS(app, supports_credentials=True)

bcrypt = Bcrypt(app)
db.init_app(app)

with app.app_context():
    db.create_all()

# Check if user is logged in
@app.route('/check_session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        return jsonify({'status': 'logged in'})
    return jsonify({'status': 'not logged in'})

@app.route('/registration', methods=['POST'])
def signup():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        return jsonify({'error': 'Email already exists.'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.id

    return jsonify({
        'id': new_user.id,
        'email': new_user.email
    })

@app.route('/login', methods=['POST'])
def login_user():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=email).first()

    if user is None or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Unauthorized'}), 401

    session['user_id'] = user.id
    return jsonify({
        'id': user.id,
        'email': email
    })

@app.route('/logout', methods=['POST'])
def logout_user():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return jsonify({'email': user.email}), 200
    return jsonify({'error': 'User not logged in'}), 401

@app.route('/search', methods=['POST'])
def search_flights_route():
    data = request.json

    sourceAirportCode = data.get('sourceAirportCode')
    destinationAirportCode = data.get('destinationAirportCode')
    date = data.get('date')
    returnDate = data.get('returnDate')
    itineraryType = data.get('itineraryType')
    sortOrder = data.get('sortOrder')
    numAdults = data.get('numAdults')
    numSeniors = data.get('numSeniors')
    classOfService = data.get('classOfService')

    if not all([sourceAirportCode, destinationAirportCode, date, returnDate, itineraryType, sortOrder, numAdults, numSeniors, classOfService]):
        return jsonify({'error': 'All fields are required.'}), 400

    try:
        flights = searchFlights(sourceAirportCode, destinationAirportCode, date, returnDate, itineraryType, sortOrder, numAdults, numSeniors, classOfService)
        return jsonify(flights)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(port=3002)
