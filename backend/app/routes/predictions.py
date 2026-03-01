import json
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.prediction import Prediction
from app.models.customer import Customer
from app.utils.decorators import login_required
from app.services.prediction_service import make_prediction
from app.services.usage_service import track_usage, check_limit

predictions_bp = Blueprint('predictions', __name__)


@predictions_bp.route('/predict', methods=['POST'])
@login_required
def predict(current_user):
    # Check plan limit
    ok, msg = check_limit(current_user, 'predictions')
    if not ok:
        return jsonify({'error': msg}), 403

    data = request.get_json()
    customer_id = data.get('customer_id')

    # Run prediction
    result = make_prediction(data)

    # Save prediction record
    prediction = Prediction(
        user_id=current_user.id,
        customer_id=customer_id,
        prediction_result=result['prediction'],
        probability=result['probability'],
        confidence_score=result['confidence'],
        risk_level=result['risk_level'],
        retention_action=result['retention_action'],
        input_data=json.dumps(data),
    )
    db.session.add(prediction)

    # Update customer record if linked
    if customer_id:
        customer = Customer.query.filter_by(id=customer_id, user_id=current_user.id).first()
        if customer:
            customer.churn_prediction = result['prediction']
            customer.churn_probability = result['probability']
            customer.risk_level = result['risk_level']

    db.session.commit()
    track_usage(current_user.id, 'predictions_used')

    return jsonify({
        'prediction': result['prediction'],
        'probability': result['probability'],
        'confidence': result['confidence'],
        'risk_level': result['risk_level'],
        'retention_action': result['retention_action'],
        'prediction_id': prediction.id,
    }), 200


@predictions_bp.route('/predictions', methods=['GET'])
@login_required
def list_predictions(current_user):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'predictions': [p.to_dict() for p in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
    }), 200
