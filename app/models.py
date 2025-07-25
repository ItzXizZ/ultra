from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class OpportunitySubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(32), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(200))
    location = db.Column(db.String(200))
    type = db.Column(db.String(100))
    application_deadline = db.Column(db.String(100))
    gpa_requirement = db.Column(db.String(20))
    skills = db.Column(db.String(300))
    grade_levels = db.Column(db.String(100))
    compensation = db.Column(db.String(100))
    file_attachment = db.Column(db.String(300))
    status = db.Column(db.String(20), default='pending')
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    priority = db.Column(db.Boolean, default=False)
    badge = db.Column(db.String(100))
    
    # New fields for submitter information
    submitter_role = db.Column(db.String(100))
    submitter_name = db.Column(db.String(200))
    submitter_email = db.Column(db.String(200))
    submitter_phone = db.Column(db.String(50))
    
    # New fields for company information
    company_website = db.Column(db.String(500))
    company_size = db.Column(db.String(100))
    industry = db.Column(db.String(200))
    company_location = db.Column(db.String(200))
    
    # New fields for application information
    application_link = db.Column(db.String(500))
    application_method = db.Column(db.String(100))
    application_instructions = db.Column(db.Text) 