from datetime import datetime
from app.extensions import db


class UsageTracking(db.Model):
    __tablename__ = 'usage_tracking'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    month = db.Column(db.String(7), nullable=False)  # 'YYYY-MM'
    predictions_used = db.Column(db.Integer, default=0)
    customers_added = db.Column(db.Integer, default=0)
    api_calls = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'month', name='uq_user_month'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'month': self.month,
            'predictions_used': self.predictions_used,
            'customers_added': self.customers_added,
            'api_calls': self.api_calls,
        }
