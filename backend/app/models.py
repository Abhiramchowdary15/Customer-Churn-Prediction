from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    tenure = db.Column(db.Integer)
    monthly_charges = db.Column(db.Float)
    churn_risk = db.Column(db.String(20)) # High, Medium, Low