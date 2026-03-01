from datetime import datetime
from app.extensions import db


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Customer info
    customer_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), default='Male')
    senior_citizen = db.Column(db.Boolean, default=False)
    partner = db.Column(db.Boolean, default=False)
    dependents = db.Column(db.Boolean, default=False)

    # Service info
    tenure = db.Column(db.Integer, default=0)
    phone_service = db.Column(db.Boolean, default=True)
    internet_service = db.Column(db.String(30), default='Fiber optic')
    contract = db.Column(db.String(30), default='Month-to-month')
    paperless_billing = db.Column(db.Boolean, default=True)
    payment_method = db.Column(db.String(50), default='Electronic check')

    # Financials
    monthly_charges = db.Column(db.Float, default=0.0)
    total_charges = db.Column(db.Float, default=0.0)

    # Satisfaction metrics
    rating = db.Column(db.Integer, default=3)          # 1-5 scale (1=Very Bad, 5=Excellent)
    feedback_score = db.Column(db.Integer, default=1)   # 0=Negative, 1=Neutral, 2=Positive
    nps_score = db.Column(db.Integer, default=7)        # 0-10 NPS scale

    # Usage frequency
    daily_logins = db.Column(db.Float, default=1.0)              # avg daily logins
    weekly_transactions = db.Column(db.Integer, default=5)        # transactions per week
    avg_session_minutes = db.Column(db.Float, default=15.0)       # avg session duration
    last_login_days = db.Column(db.Integer, default=0)            # days since last login

    # Prediction results (cached)
    churn_prediction = db.Column(db.String(20), nullable=True)   # 'Churn' / 'No Churn'
    churn_probability = db.Column(db.Float, nullable=True)
    risk_level = db.Column(db.String(20), nullable=True)          # 'High' / 'Medium' / 'Low'

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    predictions = db.relationship('Prediction', backref='customer', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'customer_name': self.customer_name,
            'gender': self.gender,
            'senior_citizen': self.senior_citizen,
            'partner': self.partner,
            'dependents': self.dependents,
            'tenure': self.tenure,
            'phone_service': self.phone_service,
            'internet_service': self.internet_service,
            'contract': self.contract,
            'paperless_billing': self.paperless_billing,
            'payment_method': self.payment_method,
            'monthly_charges': self.monthly_charges,
            'total_charges': self.total_charges,
            'rating': self.rating,
            'feedback_score': self.feedback_score,
            'nps_score': self.nps_score,
            'daily_logins': self.daily_logins,
            'weekly_transactions': self.weekly_transactions,
            'avg_session_minutes': self.avg_session_minutes,
            'last_login_days': self.last_login_days,
            'churn_prediction': self.churn_prediction,
            'churn_probability': self.churn_probability,
            'risk_level': self.risk_level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
