from app import create_app, db
from app.models import OpportunitySubmission
import sqlite3

app = create_app()

def migrate_database():
    with app.app_context():
        # Get the database connection
        conn = sqlite3.connect('app/opportunities.db')
        cursor = conn.cursor()
        
        # Add new columns to the opportunity_submission table
        new_columns = [
            'submitter_role TEXT',
            'submitter_name TEXT',
            'submitter_email TEXT', 
            'submitter_phone TEXT',
            'company_website TEXT',
            'company_size TEXT',
            'industry TEXT',
            'company_location TEXT',
            'application_link TEXT',
            'application_method TEXT',
            'application_instructions TEXT'
        ]
        
        for column_def in new_columns:
            column_name = column_def.split()[0]
            try:
                cursor.execute(f'ALTER TABLE opportunity_submission ADD COLUMN {column_def}')
                print(f"Added column: {column_name}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"Column {column_name} already exists, skipping...")
                else:
                    print(f"Error adding column {column_name}: {e}")
        
        conn.commit()
        conn.close()
        print("Database migration completed successfully!")

if __name__ == '__main__':
    migrate_database() 