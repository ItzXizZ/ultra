from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import os
from . import db, login_manager
from .models import User, OpportunitySubmission

bp = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    flash('Please log in to access this page.')
    return redirect(url_for('main.login'))

# --- Home Page ---
@bp.route('/')
def home():
    return render_template('home.html')

# --- Auth ---
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.moderate'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# --- Ultra Exclusive Submission ---
@bp.route('/submit/ultra', methods=['GET', 'POST'])
def submit_ultra():
    if request.method == 'POST':
        # Handle file upload
        file_attachment = None
        if 'file_attachment' in request.files:
            file = request.files['file_attachment']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                file_attachment = filename
        
        # Create submission with all form fields
        submission = OpportunitySubmission(
            source='ultra',
            title=request.form['title'],
            description=request.form['description'],
            company=request.form['company'],
            location=request.form.get('location'),
            type=request.form.get('type'),
            application_deadline=request.form.get('application_deadline'),
            gpa_requirement=request.form.get('gpa_requirement'),
            skills=request.form.get('skills'),
            grade_levels=request.form.get('grade_levels'),
            compensation=request.form.get('compensation'),
            file_attachment=file_attachment,
            priority=True,
            badge='Ultra Exclusive',
            
            # New submitter information fields
            submitter_role=request.form.get('submitter_role'),
            submitter_name=request.form.get('submitter_name'),
            submitter_email=request.form.get('submitter_email'),
            submitter_phone=request.form.get('submitter_phone'),
            
            # New company information fields
            company_website=request.form.get('company_website'),
            company_size=request.form.get('company_size'),
            industry=request.form.get('industry'),
            company_location=request.form.get('company_location'),
            
            # New application information fields
            application_link=request.form.get('application_link'),
            application_method=request.form.get('application_method'),
            application_instructions=request.form.get('application_instructions')
        )
        
        db.session.add(submission)
        db.session.commit()
        flash('Ultra Exclusive opportunity submitted successfully!')
        return redirect(url_for('main.submit_ultra'))
    
    return render_template('submit_ultra.html')

# --- General Submission ---
@bp.route('/submit/general', methods=['GET', 'POST'])
def submit_general():
    if request.method == 'POST':
        # Create submission with all form fields
        submission = OpportunitySubmission(
            source='general',
            title=request.form['title'],
            description=request.form['description'],
            company=request.form['company'],
            location=request.form.get('location'),
            type=request.form.get('type'),
            application_deadline=request.form.get('application_deadline'),
            
            # New submitter information fields
            submitter_role=request.form.get('submitter_role'),
            submitter_name=request.form.get('submitter_name'),
            submitter_email=request.form.get('submitter_email'),
            submitter_phone=request.form.get('submitter_phone'),
            
            # New company information fields
            company_website=request.form.get('company_website'),
            industry=request.form.get('industry'),
            
            # New application information fields
            application_link=request.form.get('application_link'),
            application_method=request.form.get('application_method'),
            application_instructions=request.form.get('application_instructions')
        )
        
        db.session.add(submission)
        db.session.commit()
        flash('General opportunity submitted successfully!')
        return redirect(url_for('main.submit_general'))
    
    return render_template('submit_general.html')

# --- Moderation Dashboard ---
@bp.route('/moderate', methods=['GET', 'POST'])
@login_required
def moderate():
    if request.method == 'POST':
        # Handle bulk actions
        if 'bulk_action' in request.form and request.form['bulk_action']:
            bulk_action = request.form['bulk_action']
            selected_items = request.form.getlist('selected_items')
            bulk_feedback = request.form.get('bulk_feedback', '')
            
            if selected_items:
                submissions = OpportunitySubmission.query.filter(OpportunitySubmission.id.in_(selected_items)).all()
                
                for submission in submissions:
                    if bulk_action == 'approve':
                        submission.status = 'approved'
                        if bulk_feedback:
                            submission.feedback = bulk_feedback
                    elif bulk_action == 'reject':
                        submission.status = 'rejected'
                        if bulk_feedback:
                            submission.feedback = bulk_feedback
                    elif bulk_action == 'delete':
                        db.session.delete(submission)
                
                db.session.commit()
                flash(f'Bulk action "{bulk_action}" completed on {len(selected_items)} items!')
                return redirect(url_for('main.moderate'))
        
        # Handle individual actions
        sub_id = request.form.get('id')
        action = request.form.get('action')
        
        if sub_id and action:
            submission = OpportunitySubmission.query.get(sub_id)

            if submission:
                if action == 'approve':
                    submission.status = 'approved'
                    feedback = request.form.get('feedback', '')
                    if feedback:
                        submission.feedback = feedback
                    flash(f'Submission "{submission.title}" approved!')

                elif action == 'reject':
                    submission.status = 'rejected'
                    feedback = request.form.get('feedback', '')
                    if feedback:
                        submission.feedback = feedback
                    flash(f'Submission "{submission.title}" rejected!')

                elif action == 'edit':
                    submission.title = request.form.get('title', submission.title)
                    submission.description = request.form.get('description', submission.description)
                    submission.company = request.form.get('company', submission.company)
                    submission.location = request.form.get('location', submission.location)
                    submission.type = request.form.get('type', submission.type)
                    submission.application_deadline = request.form.get('application_deadline', submission.application_deadline)
                    
                    # Additional fields
                    submission.gpa_requirement = request.form.get('gpa_requirement', submission.gpa_requirement)
                    submission.skills = request.form.get('skills', submission.skills)
                    submission.grade_levels = request.form.get('grade_levels', submission.grade_levels)
                    submission.compensation = request.form.get('compensation', submission.compensation)
                    
                    # Submitter information
                    submission.submitter_role = request.form.get('submitter_role', submission.submitter_role)
                    submission.submitter_name = request.form.get('submitter_name', submission.submitter_name)
                    submission.submitter_email = request.form.get('submitter_email', submission.submitter_email)
                    submission.submitter_phone = request.form.get('submitter_phone', submission.submitter_phone)
                    
                    # Company information
                    submission.company_website = request.form.get('company_website', submission.company_website)
                    submission.company_size = request.form.get('company_size', submission.company_size)
                    submission.industry = request.form.get('industry', submission.industry)
                    submission.company_location = request.form.get('company_location', submission.company_location)
                    
                    # Application information
                    submission.application_link = request.form.get('application_link', submission.application_link)
                    submission.application_method = request.form.get('application_method', submission.application_method)
                    submission.application_instructions = request.form.get('application_instructions', submission.application_instructions)
                    
                    # Priority and badge
                    priority_value = request.form.get('priority', 'False')
                    submission.priority = priority_value == 'True'
                    submission.badge = request.form.get('badge', submission.badge)
                    
                    flash(f'Submission "{submission.title}" updated!')

                elif action == 'delete':
                    title = submission.title
                    db.session.delete(submission)
                    flash(f'Submission "{title}" deleted!')

                db.session.commit()

    # Build query with filters
    query = OpportunitySubmission.query
    
    # Status filter
    status_filter = request.args.get('status')
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    # Source filter
    source_filter = request.args.get('source')
    if source_filter:
        query = query.filter_by(source=source_filter)
    
    # Search filter
    search_filter = request.args.get('search')
    if search_filter:
        query = query.filter(
            (OpportunitySubmission.title.contains(search_filter)) |
            (OpportunitySubmission.company.contains(search_filter))
        )
    
    # Get submissions
    submissions = query.order_by(OpportunitySubmission.created_at.desc()).all()
    
    # Calculate statistics
    stats = {
        'pending': OpportunitySubmission.query.filter_by(status='pending').count(),
        'approved': OpportunitySubmission.query.filter_by(status='approved').count(),
        'rejected': OpportunitySubmission.query.filter_by(status='rejected').count(),
        'total': OpportunitySubmission.query.count()
    }
    
    return render_template('moderate.html', submissions=submissions, stats=stats)

# --- Serve Uploaded Files ---
@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

# --- Opportunities Page ---
@bp.route('/opportunities')
def opportunities():
    approved_opportunities = OpportunitySubmission.query.filter_by(status='approved').order_by(OpportunitySubmission.created_at.desc()).all()
    return render_template('opportunities.html', opportunities=approved_opportunities) 