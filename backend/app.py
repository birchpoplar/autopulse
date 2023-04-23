from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Car
from datetime import datetime

app = Flask(__name__)

# Configure your SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Enable CORS for the frontend
CORS(app)

# Import your models
# from models import Car, Service

# Create the database tables (only run once, then comment out or remove this line)
# db.create_all()

@app.route('/')
def home():
    return "Car Mileage and Servicing Tracker API"

@app.route('/register_car', methods=['POST'])
def register_car():
    try:
        # Extract the car data from the request JSON
        car_data = request.get_json()

        last_service_date = datetime.strptime(car_data['last_service_date'], "%Y-%m-%d").date()

        # Create a new Car instance with the provided data
        new_car = Car(
            make=car_data['make'],
            model=car_data['model'],
            year=car_data['year'],
            mileage=car_data['mileage'],
            last_service_date=last_service_date
        )

        # Add the new car to the database and commit the changes
        db.session.add(new_car)
        db.session.commit()

        # Return a success message and the new car's ID
        response = {
            'message': 'Car registered successfully.',
            'car_id': new_car.id
        }
        return jsonify(response), 201
    except Exception as e:
        # In case of an error, return an error message
        response = {
            'message': f'An error occurred while registering the car: {str(e)}'
        }
        return jsonify(response), 400

@app.route('/update_last_service_date', methods=['POST'])
def update_last_service_date():
    data = request.get_json()

    car_id = data.get('car_id')
    new_last_service_date = data.get('new_last_service_date')

    if not car_id or not new_last_service_date:
        return jsonify({"message": "Both car_id and new_last_service_date are required."}), 400

    # Convert the new_last_service_date string to a date object
    new_last_service_date = datetime.strptime(new_last_service_date, "%Y-%m-%d").date()

    car = Car.query.get(car_id)
    if not car:
        return jsonify({"message": "Car not found."}), 404

    car.last_service_date = new_last_service_date
    db.session.commit()

    return jsonify({"message": "Last service date updated successfully."})

@app.route('/list_cars', methods=['GET'])
def list_cars():
    cars = Car.query.all()
    result = []

    for car in cars:
        car_data = {
            'id': car.id,
            'make': car.make,
            'model': car.model,
            'year': car.year,
            'mileage': car.mileage,
            'last_service_date': car.last_service_date.strftime("%Y-%m-%d")
        }
        result.append(car_data)

    return jsonify(result)

# @app.route('/update_mileage', methods=['PUT'])
# def update_mileage():
#     # Your logic for updating car mileage
#     pass

# @app.route('/check_service', methods=['GET'])
# def check_service():
#     # Your logic for checking if service is required
#     pass

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)