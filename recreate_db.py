from app import create_app, db
from app.models import User, OpportunitySubmission
from werkzeug.security import generate_password_hash
import os

app = create_app()

def recreate_database():
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        # Create admin user
        admin = User(username='admin', password_hash=generate_password_hash('password'))
        db.session.add(admin)
        db.session.commit()
        
        print("Database recreated successfully with new schema!")
        print("Admin user created: username='admin', password='password'")

if __name__ == '__main__':
    # Remove existing database file
    db_path = 'app/opportunities.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    recreate_database() 