#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Migration Script
Adds the 'daily_routine_medications' column to the responses table
"""

import sqlite3
import os
from datetime import datetime

DATABASE = 'questionnaire.db'

def backup_database():
    """Create a backup of the database before migration"""
    if os.path.exists(DATABASE):
        backup_name = f"questionnaire.db.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        import shutil
        shutil.copy2(DATABASE, backup_name)
        print(f"[OK] Backup created: {backup_name}")
        return backup_name
    return None

def migrate():
    """Add daily_routine_medications column to responses table"""
    if not os.path.exists(DATABASE):
        print(f"[ERROR] Database not found: {DATABASE}")
        print("  The database will be created automatically when you run the application.")
        return

    # Create backup
    backup_file = backup_database()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(responses)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'daily_routine_medications' not in columns:
            print("Adding 'daily_routine_medications' column to responses table...")
            cursor.execute("ALTER TABLE responses ADD COLUMN daily_routine_medications TEXT")
            conn.commit()
            print("[OK] Migration completed successfully!")
            print("  New column 'daily_routine_medications' added")
        else:
            print("[OK] Column 'daily_routine_medications' already exists")
            print("  No migration needed")

        # Verify the migration
        cursor.execute("PRAGMA table_info(responses)")
        columns = cursor.fetchall()
        print("\nCurrent table schema:")
        print("-" * 50)
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        print("-" * 50)

    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")
        conn.rollback()
        if backup_file:
            print(f"\n  You can restore from backup: {backup_file}")
        raise

    finally:
        conn.close()

def main():
    print("=" * 50)
    print("Database Migration: Add daily_routine_medications")
    print("=" * 50)
    print()

    try:
        migrate()
        print()
        print("[OK] Migration completed successfully!")
        print()
        print("You can now run the application:")
        print("  python app.py")
    except Exception as e:
        print()
        print("[ERROR] Migration failed!")
        print(f"  Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
