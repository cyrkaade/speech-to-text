# Database Migration Note

## New Column Added: `daily_routine_medications`

### Change Summary
A new question has been added to the questionnaire: **"Как прошел ваш день и какие таблетки вы пили?"** (How was your day and what pills did you take?)

This requires a new column in the database to store the answer.

### Schema Change

**New Column:**
- `daily_routine_medications TEXT`

**Updated Schema:**
```sql
CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    weight TEXT,
    heart_rate TEXT,
    edema TEXT,
    smoking_status TEXT,
    cigarette_count TEXT,
    daily_routine_medications TEXT,  -- NEW COLUMN
    ai_score INTEGER,
    ai_feedback TEXT
)
```

## Migration Options

### Option 1: Automatic Migration (Recommended for Development)

If you're in development and don't have important data:

1. **Delete the existing database:**
   ```bash
   rm questionnaire.db
   ```

2. **Restart the application:**
   ```bash
   python app.py
   ```
   The database will be recreated with the new schema automatically.

### Option 2: Manual Migration (Recommended for Production)

If you have existing data you want to preserve:

1. **Create a backup:**
   ```bash
   cp questionnaire.db questionnaire.db.backup
   ```

2. **Add the new column manually:**
   ```bash
   sqlite3 questionnaire.db
   ```

3. **Run this SQL command:**
   ```sql
   ALTER TABLE responses ADD COLUMN daily_routine_medications TEXT;
   ```

4. **Exit SQLite:**
   ```
   .exit
   ```

5. **Restart the application:**
   ```bash
   python app.py
   ```

### Option 3: Python Migration Script

Create and run this migration script:

```python
# migrate_db.py
import sqlite3

DATABASE = 'questionnaire.db'

def migrate():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(responses)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'daily_routine_medications' not in columns:
            print("Adding daily_routine_medications column...")
            cursor.execute("ALTER TABLE responses ADD COLUMN daily_routine_medications TEXT")
            conn.commit()
            print("✓ Migration completed successfully!")
        else:
            print("✓ Column already exists, no migration needed.")

    except Exception as e:
        print(f"✗ Migration failed: {e}")
        conn.rollback()

    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
```

Run it:
```bash
python migrate_db.py
```

## Verification

After migration, verify the schema:

```bash
sqlite3 questionnaire.db ".schema responses"
```

You should see the `daily_routine_medications` column in the output.

## Testing the New Question

1. Start the application:
   ```bash
   python app.py
   ```

2. Navigate to: http://localhost:5000/questionnaire

3. Fill out all 6 questions (the new question is #6)

4. Test with medicament recognition:
   - Record: "День прошел хорошо, принимал Аспирин утром и Омепразол вечером"
   - Verify: Medicament names are correctly transcribed

5. Submit the questionnaire and check the feedback includes analysis of medications

## Rollback (If Needed)

If you need to rollback:

1. Restore from backup:
   ```bash
   cp questionnaire.db.backup questionnaire.db
   ```

2. Revert code changes to the previous version

## Notes

- The new column is nullable (TEXT type with no NOT NULL constraint)
- Existing records will have NULL for `daily_routine_medications`
- The AI feedback function now includes this field in its analysis
- The medicament recognition will work automatically for this question

---

**Migration Status:** Required before using the updated application
**Breaking Change:** No (backward compatible with NULL values)
**Data Loss Risk:** None (if using manual migration with backup)
