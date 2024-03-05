import sqlite3


def execute():
    # Step a: Create a SQLite database
    db_name = 'image_generation.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Step b: Create a job_queue table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS job_queue (
        id INTEGER PRIMARY KEY,
        prompt TEXT NOT NULL,
        status TEXT NOT NULL
    )
    ''')

    # Step c: Create a result table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS result (
        id INTEGER PRIMARY KEY,
        prompt TEXT NOT NULL,
        timestamp DATETIME NOT NULL,
        image BLOB NOT NULL
    )
    ''')

    # Commit the changes and close the connection to the database
    conn.commit()
    conn.close()

    print(f"Database '{db_name}' and tables 'job_queue' and 'result' created successfully.")
