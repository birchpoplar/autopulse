from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Float, nullable=False)
    last_service_date = db.Column(db.Date, nullable=False)

    def __init__(self, make, model, year, mileage, last_service_date):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.last_service_date = last_service_date

    def __repr__(self):
        return f"<Car {self.make} {self.model} ({self.year})>"
