from datetime import datetime
from app.extensions import db
from app.models.usage import UsageTracking
from app.models.subscription import SubscriptionPlan
from app.models.customer import Customer
from app.models.prediction import Prediction


def get_or_create_usage(user_id):
    """Get or create usage record for the current month."""
    month_str = datetime.utcnow().strftime('%Y-%m')
    usage = UsageTracking.query.filter_by(user_id=user_id, month=month_str).first()
    if not usage:
        usage = UsageTracking(user_id=user_id, month=month_str)
        db.session.add(usage)
        db.session.commit()
    return usage


def track_usage(user_id, metric, count=1):
    """Increment a usage metric for the current month."""
    usage = get_or_create_usage(user_id)
    if metric == 'predictions_used':
        usage.predictions_used += count
    elif metric == 'customers_added':
        usage.customers_added += count
    elif metric == 'api_calls':
        usage.api_calls += count
    usage.api_calls += 1  # Every tracked action counts as an API call
    db.session.commit()


def check_limit(user, limit_type):
    """Check if the user has exceeded their plan limits.

    Returns (ok: bool, message: str).
    """
    plan = SubscriptionPlan.query.filter_by(name=user.plan).first()
    if not plan:
        return True, ''  # No plan restrictions if plan not found

    if limit_type == 'customers':
        current_count = Customer.query.filter_by(user_id=user.id).count()
        if current_count >= plan.max_customers:
            return False, f'Customer limit reached ({plan.max_customers}). Upgrade your plan.'
    elif limit_type == 'predictions':
        usage = get_or_create_usage(user.id)
        if usage.predictions_used >= plan.max_predictions:
            return False, f'Monthly prediction limit reached ({plan.max_predictions}). Upgrade your plan.'

    return True, ''
