import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/opportunities.db')
cursor = conn.cursor()

# Show all tables
print("=== DATABASE TABLES ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
for table in tables:
    print(f"Table: {table[0]}")

# Show opportunity submissions
print("\n=== OPPORTUNITY SUBMISSIONS ===")
try:
    cursor.execute("SELECT * FROM opportunity_submission")
    submissions = cursor.fetchall()
    print(f"Total submissions: {len(submissions)}")
    
    # Get column names
    cursor.execute("PRAGMA table_info(opportunity_submission)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Columns: {columns}")
    
    # Show first few submissions
    for i, submission in enumerate(submissions[:3]):
        print(f"\nSubmission {i+1}:")
        for j, value in enumerate(submission):
            print(f"  {columns[j]}: {value}")
            
except Exception as e:
    print(f"Error reading submissions: {e}")

# Show users
print("\n=== USERS ===")
try:
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    print(f"Total users: {len(users)}")
    for user in users:
        print(f"User: {user}")
except Exception as e:
    print(f"Error reading users: {e}")

conn.close() 