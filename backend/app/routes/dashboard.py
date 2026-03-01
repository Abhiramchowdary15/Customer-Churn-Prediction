from flask import Blueprint, jsonify
from sqlalchemy import func
from app.extensions import db
from app.models.customer import Customer
from app.models.prediction import Prediction
from app.models.usage import UsageTracking
from app.utils.decorators import login_required
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/stats', methods=['GET'])
@login_required
def get_stats(current_user):
    uid = current_user.id

    # KPI counts
    total_customers = Customer.query.filter_by(user_id=uid).count()
    active_customers = Customer.query.filter(
        Customer.user_id == uid,
        (Customer.churn_prediction != 'Churn') | (Customer.churn_prediction.is_(None))
    ).count()
    churn_customers = Customer.query.filter_by(user_id=uid, churn_prediction='Churn').count()
    churn_pct = round((churn_customers / total_customers * 100), 1) if total_customers > 0 else 0

    # Revenue at risk
    churn_revenue = db.session.query(func.coalesce(func.sum(Customer.monthly_charges), 0)).filter(
        Customer.user_id == uid, Customer.churn_prediction == 'Churn'
    ).scalar()

    # API usage this month
    month_str = datetime.utcnow().strftime('%Y-%m')
    usage = UsageTracking.query.filter_by(user_id=uid, month=month_str).first()
    api_usage = usage.api_calls if usage else 0
    predictions_used = usage.predictions_used if usage else 0

    # Average satisfaction (composite of rating and NPS)
    avg_rating = db.session.query(func.coalesce(func.avg(Customer.rating), 0)).filter_by(user_id=uid).scalar()
    avg_nps = db.session.query(func.coalesce(func.avg(Customer.nps_score), 0)).filter_by(user_id=uid).scalar()
    avg_satisfaction = round((float(avg_rating) / 5 * 50) + (float(avg_nps) / 10 * 50), 1) if total_customers > 0 else 0

    # Average engagement (usage frequency composite)
    avg_logins = db.session.query(func.coalesce(func.avg(Customer.daily_logins), 0)).filter_by(user_id=uid).scalar()
    avg_trans = db.session.query(func.coalesce(func.avg(Customer.weekly_transactions), 0)).filter_by(user_id=uid).scalar()
    avg_session = db.session.query(func.coalesce(func.avg(Customer.avg_session_minutes), 0)).filter_by(user_id=uid).scalar()
    avg_engagement = round(
        (min(float(avg_logins), 10) / 10 * 0.3 +
         min(float(avg_trans), 30) / 30 * 0.3 +
         min(float(avg_session), 120) / 120 * 0.4) * 100, 1
    ) if total_customers > 0 else 0

    # Chart data: churn by contract type
    contract_data = db.session.query(
        Customer.contract, func.count(Customer.id)
    ).filter_by(user_id=uid).group_by(Customer.contract).all()

    # Chart data: churn by internet service
    internet_data = db.session.query(
        Customer.internet_service,
        func.count(Customer.id),
        func.sum(db.case((Customer.churn_prediction == 'Churn', 1), else_=0))
    ).filter_by(user_id=uid).group_by(Customer.internet_service).all()

    # Chart data: risk distribution
    risk_data = db.session.query(
        Customer.risk_level, func.count(Customer.id)
    ).filter(Customer.user_id == uid, Customer.risk_level.isnot(None)).group_by(Customer.risk_level).all()

    # Chart data: monthly prediction trends (last 6 months)
    trend_data = db.session.query(
        func.date_format(Prediction.created_at, '%Y-%m').label('month'),
        func.count(Prediction.id).label('total'),
        func.sum(db.case((Prediction.prediction_result == 'Churn', 1), else_=0)).label('churn_count')
    ).filter_by(user_id=uid).group_by('month').order_by('month').limit(6).all()

    # Chart data: satisfaction distribution (rating breakdown)
    satisfaction_data = db.session.query(
        Customer.rating, func.count(Customer.id)
    ).filter_by(user_id=uid).group_by(Customer.rating).order_by(Customer.rating).all()

    rating_labels = {1: 'Very Bad', 2: 'Bad', 3: 'Neutral', 4: 'Good', 5: 'Excellent'}

    return jsonify({
        'kpis': {
            'total_customers': total_customers,
            'active_customers': active_customers,
            'churn_percentage': churn_pct,
            'revenue_at_risk': round(float(churn_revenue), 2),
            'api_usage': api_usage,
            'predictions_used': predictions_used,
            'avg_satisfaction': avg_satisfaction,
            'avg_rating': round(float(avg_rating), 1),
            'avg_nps': round(float(avg_nps), 1),
            'avg_engagement': avg_engagement,
        },
        'charts': {
            'contract_distribution': [
                {'name': c[0] or 'Unknown', 'value': c[1]} for c in contract_data
            ],
            'internet_churn': [
                {'name': c[0] or 'Unknown', 'total': c[1], 'churn': int(c[2] or 0)} for c in internet_data
            ],
            'risk_distribution': [
                {'name': r[0], 'value': r[1]} for r in risk_data
            ],
            'churn_trends': [
                {'month': t[0], 'total': t[1], 'churn': int(t[2] or 0)} for t in trend_data
            ],
            'satisfaction_distribution': [
                {'name': rating_labels.get(s[0], f'Rating {s[0]}'), 'value': s[1], 'rating': s[0]} for s in satisfaction_data
            ],
        },
    }), 200
