from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'  # Change in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///opportunities.db'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB upload limit

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Import models to ensure they're registered with SQLAlchemy
    from . import models

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    from . import routes
    app.register_blueprint(routes.bp)

    # Initialize database tables
    with app.app_context():
        db.create_all()
        
        # Create admin user if it doesn't exist
        from werkzeug.security import generate_password_hash
        
        admin_user = models.User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = models.User(
                username='admin',
                password_hash=generate_password_hash('password')
            )
            db.session.add(admin_user)
            db.session.commit()

    return app 