import sqlite3
from datetime import datetime

DATABASE = 'questionnaire.db'

def view_all_responses():
    """View all questionnaire responses from the database"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, submission_time, weight, heart_rate, edema, smoking_status,
               cigarette_count, ai_score, ai_feedback
        FROM responses
        ORDER BY submission_time DESC
    ''')

    results = cursor.fetchall()
    conn.close()

    if not results:
        print("No responses found in database.")
        return

    print("=" * 100)
    print(f"Total responses: {len(results)}")
    print("=" * 100)

    for row in results:
        print(f"\nID: {row[0]}")
        print(f"Submission Time: {row[1]}")
        print(f"Weight: {row[2]}")
        print(f"Heart Rate: {row[3]}")
        print(f"Edema: {row[4]}")
        print(f"Smoking Status: {row[5]}")
        print(f"Cigarette Count: {row[6]}")
        print(f"AI Risk Score: {row[7]}/100")
        print(f"AI Feedback: {row[8]}")
        print("-" * 100)

if __name__ == '__main__':
    view_all_responses()
