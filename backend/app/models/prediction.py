from datetime import datetime
from app.extensions import db


class Prediction(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True, index=True)

    # Prediction results
    prediction_result = db.Column(db.String(20), nullable=False)   # 'Churn' / 'No Churn'
    probability = db.Column(db.Float, nullable=False)
    confidence_score = db.Column(db.Float, nullable=True)
    risk_level = db.Column(db.String(20), nullable=True)
    retention_action = db.Column(db.String(255), nullable=True)

    # Input snapshot (for history)
    input_data = db.Column(db.Text, nullable=True)  # JSON string of input features

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'customer_id': self.customer_id,
            'prediction_result': self.prediction_result,
            'probability': self.probability,
            'confidence_score': self.confidence_score,
            'risk_level': self.risk_level,
            'retention_action': self.retention_action,
            'input_data': self.input_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
