from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    
    # Create admin user if it doesn't exist
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', password_hash=generate_password_hash('password'))
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: username='admin', password='password'")
    else:
        print("Admin user already exists")
    
    print("Database initialized successfully!") 