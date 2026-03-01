import csv
import io
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.customer import Customer
from app.utils.decorators import login_required
from app.services.usage_service import track_usage, check_limit

customers_bp = Blueprint('customers', __name__)


@customers_bp.route('', methods=['GET'])
@login_required
def list_customers(current_user):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)
    sort_by = request.args.get('sort_by', 'created_at', type=str)
    sort_dir = request.args.get('sort_dir', 'desc', type=str)
    risk_filter = request.args.get('risk_level', '', type=str)
    contract_filter = request.args.get('contract', '', type=str)

    query = Customer.query.filter_by(user_id=current_user.id)

    # Search
    if search:
        query = query.filter(Customer.customer_name.ilike(f'%{search}%'))

    # Filters
    if risk_filter:
        query = query.filter_by(risk_level=risk_filter)
    if contract_filter:
        query = query.filter_by(contract=contract_filter)

    # Sort
    allowed_sorts = ['customer_name', 'tenure', 'monthly_charges', 'total_charges',
                      'churn_probability', 'risk_level', 'created_at']
    if sort_by in allowed_sorts:
        col = getattr(Customer, sort_by)
        query = query.order_by(col.desc() if sort_dir == 'desc' else col.asc())
    else:
        query = query.order_by(Customer.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'customers': [c.to_dict() for c in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'per_page': per_page,
    }), 200


@customers_bp.route('', methods=['POST'])
@login_required
def create_customer(current_user):
    # Check plan limit
    ok, msg = check_limit(current_user, 'customers')
    if not ok:
        return jsonify({'error': msg}), 403

    data = request.get_json()
    customer = Customer(
        user_id=current_user.id,
        customer_name=data.get('customer_name', 'Unknown'),
        gender=data.get('gender', 'Male'),
        senior_citizen=data.get('senior_citizen', False),
        partner=data.get('partner', False),
        dependents=data.get('dependents', False),
        tenure=int(data.get('tenure', 0)),
        phone_service=data.get('phone_service', True),
        internet_service=data.get('internet_service', 'Fiber optic'),
        contract=data.get('contract', 'Month-to-month'),
        paperless_billing=data.get('paperless_billing', True),
        payment_method=data.get('payment_method', 'Electronic check'),
        monthly_charges=float(data.get('monthly_charges', 0)),
        total_charges=float(data.get('total_charges', 0)),
        rating=max(1, min(5, int(data.get('rating', 3)))),
        feedback_score=max(0, min(2, int(data.get('feedback_score', 1)))),
        nps_score=max(0, min(10, int(data.get('nps_score', 7)))),
        daily_logins=max(0, float(data.get('daily_logins', 1.0))),
        weekly_transactions=max(0, int(data.get('weekly_transactions', 5))),
        avg_session_minutes=max(0, float(data.get('avg_session_minutes', 15.0))),
        last_login_days=max(0, int(data.get('last_login_days', 0))),
    )
    db.session.add(customer)
    db.session.commit()

    track_usage(current_user.id, 'customers_added')
    return jsonify({'message': 'Customer created', 'customer': customer.to_dict()}), 201


@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@login_required
def update_customer(customer_id, current_user):
    customer = Customer.query.filter_by(id=customer_id, user_id=current_user.id).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    data = request.get_json()
    updatable = ['customer_name', 'gender', 'senior_citizen', 'partner', 'dependents',
                 'tenure', 'phone_service', 'internet_service', 'contract',
                 'paperless_billing', 'payment_method', 'monthly_charges', 'total_charges',
                 'rating', 'feedback_score', 'nps_score',
                 'daily_logins', 'weekly_transactions', 'avg_session_minutes', 'last_login_days']
    for field in updatable:
        if field in data:
            setattr(customer, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Customer updated', 'customer': customer.to_dict()}), 200


@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
@login_required
def delete_customer(customer_id, current_user):
    customer = Customer.query.filter_by(id=customer_id, user_id=current_user.id).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted'}), 200


@customers_bp.route('/upload', methods=['POST'])
@login_required
def upload_csv(current_user):
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be CSV'}), 400

    stream = io.StringIO(file.stream.read().decode('utf-8'))
    reader = csv.DictReader(stream)

    count = 0
    errors = []
    for i, row in enumerate(reader):
        try:
            customer = Customer(
                user_id=current_user.id,
                customer_name=row.get('customer_name', row.get('name', f'Customer {i+1}')),
                gender=row.get('gender', 'Male'),
                senior_citizen=row.get('senior_citizen', '0') in ('1', 'True', 'true', 'Yes'),
                partner=row.get('partner', '0') in ('1', 'True', 'true', 'Yes'),
                dependents=row.get('dependents', '0') in ('1', 'True', 'true', 'Yes'),
                tenure=int(float(row.get('tenure', 0))),
                phone_service=row.get('phone_service', '1') not in ('0', 'False', 'false', 'No'),
                internet_service=row.get('internet_service', 'Fiber optic'),
                contract=row.get('contract', 'Month-to-month'),
                paperless_billing=row.get('paperless_billing', '1') not in ('0', 'False', 'false', 'No'),
                payment_method=row.get('payment_method', 'Electronic check'),
                monthly_charges=float(row.get('monthly_charges', 0)),
                total_charges=float(row.get('total_charges', 0)),
                rating=max(1, min(5, int(float(row.get('rating', 3))))),
                feedback_score=max(0, min(2, int(float(row.get('feedback_score', 1))))),
                nps_score=max(0, min(10, int(float(row.get('nps_score', 7))))),
                daily_logins=max(0, float(row.get('daily_logins', 1.0))),
                weekly_transactions=max(0, int(float(row.get('weekly_transactions', 5)))),
                avg_session_minutes=max(0, float(row.get('avg_session_minutes', 15.0))),
                last_login_days=max(0, int(float(row.get('last_login_days', 0)))),
            )
            db.session.add(customer)
            count += 1
        except Exception as e:
            errors.append(f'Row {i+1}: {str(e)}')

    db.session.commit()
    track_usage(current_user.id, 'customers_added', count)

    return jsonify({
        'message': f'{count} customers imported',
        'imported': count,
        'errors': errors[:10],  # Return max 10 errors
    }), 200
