"""
Seed an admin user for the application.
Run: cd backend && .venv/Scripts/python -m ml.seed_admin
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.extensions import db, bcrypt
from app.models.user import User

app = create_app()

with app.app_context():
    email = 'admin@predictloyal.com'
    existing = User.query.filter_by(email=email).first()

    if existing:
        existing.role = 'admin'
        db.session.commit()
        print(f'Updated {email} to admin role.')
    else:
        hashed = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(
            email=email,
            password_hash=hashed,
            name='Admin',
            role='admin',
            plan='Enterprise',
        )
        db.session.add(admin)
        db.session.commit()
        print(f'Created admin user: {email} / admin123')

    print('Done!')
