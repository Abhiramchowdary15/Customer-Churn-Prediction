from app.extensions import db


class SubscriptionPlan(db.Model):
    __tablename__ = 'subscription_plans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False, default=0)
    max_customers = db.Column(db.Integer, nullable=False, default=50)
    max_predictions = db.Column(db.Integer, nullable=False, default=100)
    features = db.Column(db.Text, nullable=True)  # Comma-separated feature list

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'max_customers': self.max_customers,
            'max_predictions': self.max_predictions,
            'features': self.features.split(',') if self.features else [],
        }
