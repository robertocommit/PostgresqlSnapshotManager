import os
import psycopg2

class DatabaseManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT']
        )
    
    def close(self):
        self.conn.close()

    def log_cron_execution(self, job_name, status, error_message=None, error_traceback=None):
        query = """
            INSERT INTO cron_job_log (
                job_name, 
                status, 
                error_message, 
                error_traceback
            )
            VALUES (%s, %s, %s, %s)
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, (job_name, status, error_message, error_traceback))
            self.conn.commit()
