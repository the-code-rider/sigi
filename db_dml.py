import sqlite3
from datetime import datetime
import pandas as pd


class DBDML:

    def __init__(self, db_path='image_generation.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.TODO = 'TODO'

    # Function to add an entry to the job_queue table
    def add_to_job_queue(self, prompt, status):
        # Connect to the SQLite database

        # SQL query to insert a new entry into the job_queue table
        query = '''INSERT INTO job_queue (prompt, status) VALUES (?, ?)'''
        self.cursor.execute(query, (prompt, status))
        self.conn.commit()

    def add_to_result(self, prompt, image):
        # Get the current timestamp
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # SQL query to insert a new entry into the result table
        query = '''INSERT INTO result (prompt, timestamp, image) VALUES (?, ?, ?)'''
        self.cursor.execute(query, (prompt, current_time, image))
        self.conn.commit()

    def get_pending_jobs(self):
        query = '''SELECT id, prompt, status FROM job_queue WHERE status = ?'''
        self.cursor.execute(query, ('TODO',))

        # Fetch all rows that match the query
        jobs = self.cursor.fetchall()
        return jobs

    def get_job_by_status(self, status):
        if status == 'ALL':
            query = f'SELECT id, prompt, status FROM job_queue'
        else:
            query = f'SELECT id, prompt, status FROM job_queue where status="{status}"'

        df = pd.read_sql_query(query, self.conn)
        return df

    def update_job_status(self, job_id, status):
        # SQL query to update the status of a specific job by id
        query = '''UPDATE job_queue SET status = ? WHERE id = ?'''
        self.cursor.execute(query, (status, job_id))

        # Commit the changes and close the connection
        self.conn.commit()

    def get_images(self):
        query = f'SELECT * FROM result'
        df = pd.read_sql_query(query, self.conn)
        return df



