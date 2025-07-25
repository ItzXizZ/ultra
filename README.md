# UltraU Opportunity Submission Portal (MVP)

## Features
- Ultra Exclusive, General, and Extension submission pathways
- Unified moderation dashboard for coordinators
- Public list of approved opportunities

## Setup
1. Create a virtual environment and activate it:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Mac/Linux
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```
   python
   >>> from app import create_app, db
   >>> app = create_app()
   >>> app.app_context().push()
   >>> db.create_all()
   >>> from app.models import User
   >>> from werkzeug.security import generate_password_hash
   >>> user = User(username='admin', password_hash=generate_password_hash('password'))
   >>> db.session.add(user)
   >>> db.session.commit()
   >>> exit()
   ```
4. Run the app:
   ```
   python run.py
   ```

## Usage
- Visit `/login` to log in as a coordinator (Ultra Exclusive, moderation)
- Visit `/submit/general` for public submissions
- POST to `/submit/extension` for extension submissions
- Visit `/moderate` for the moderation dashboard
- Visit `/opportunities` to see approved opportunities

## Notes
- Uploaded files are stored in `app/uploads/`
- Default coordinator login: `admin` / `password` 