from flask import Blueprint, jsonify
from sqlalchemy import func
from app.extensions import db
from app.models.user import User
from app.models.customer import Customer
from app.models.prediction import Prediction
from app.models.subscription import SubscriptionPlan
from app.models.usage import UsageTracking
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users(current_user):
    users = User.query.order_by(User.created_at.desc()).all()
    result = []
    for u in users:
        customer_count = Customer.query.filter_by(user_id=u.id).count()
        prediction_count = Prediction.query.filter_by(user_id=u.id).count()
        result.append({
            **u.to_dict(),
            'customer_count': customer_count,
            'prediction_count': prediction_count,
        })
    return jsonify({'users': result}), 200


@admin_bp.route('/analytics', methods=['GET'])
@admin_required
def system_analytics(current_user):
    total_users = User.query.count()
    total_customers = Customer.query.count()
    total_predictions = Prediction.query.count()

    # Plan distribution
    plan_dist = db.session.query(
        User.plan, func.count(User.id)
    ).group_by(User.plan).all()

    # Role distribution
    role_dist = db.session.query(
        User.role, func.count(User.id)
    ).group_by(User.role).all()

    # Recent signups (last 7 days)
    from datetime import datetime, timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_signups = User.query.filter(User.created_at >= week_ago).count()

    return jsonify({
        'total_users': total_users,
        'total_customers': total_customers,
        'total_predictions': total_predictions,
        'recent_signups': recent_signups,
        'plan_distribution': [{'name': p[0], 'value': p[1]} for p in plan_dist],
        'role_distribution': [{'name': r[0], 'value': r[1]} for r in role_dist],
    }), 200


@admin_bp.route('/plans', methods=['GET'])
@admin_required
def list_plans(current_user):
    plans = SubscriptionPlan.query.all()
    return jsonify({'plans': [p.to_dict() for p in plans]}), 200
