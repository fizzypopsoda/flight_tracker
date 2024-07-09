from flask import Flask, request, jsonify, session
from flask_cors import CORS
from models import User, db
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Configure your Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///flaskdb.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret_key') #gonna make this

CORS(app)

bcrypt = Bcrypt(app)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/registration", methods=['POST'])
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

    if user is None:
        return jsonify({'error': 'Unauthorized access'}), 401
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Unauthorized'}), 401

    session['user_id'] = user.id

    return jsonify({
        'id': user.id,
        'email': email
    })

if __name__ == '__main__':
    app.run(port=3001)