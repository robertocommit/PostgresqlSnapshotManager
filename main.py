import os
import boto3
import traceback
import subprocess
from db_manager import DatabaseManager
from email_monitoring import send_email
from datetime import datetime, timedelta
from botocore.exceptions import NoCredentialsError

def delete_old_dumps(directory, days=7):
    print(f"Checking for dump files older than {days} days to delete...")
    now = datetime.now()
    for filename in os.listdir(directory):
        if filename.endswith('.dump'):
            file_path = os.path.join(directory, filename)
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if now - file_mod_time > timedelta(days=days):
                os.remove(file_path)
                print(f"Deleted old dump file: {filename}")

def upload_to_s3(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name
    s3_client = boto3.client('s3')
    try:
        print(f"Uploading {file_name} to bucket {bucket} as {object_name}...")
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"Successfully uploaded {file_name} to {bucket}/{object_name}")
    except NoCredentialsError:
        print("AWS credentials not available")
        raise
    except Exception as e:
        print(f"Failed to upload {file_name} to S3: {e}")
        raise

def main(db):
    DB_DUMP_JOB_NAME = 'DBDump'
    DUMP_FILE_PREFIX = 'export'
    DUMP_FILE_EXTENSION = '.dump'
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    dump_file = f"{DUMP_FILE_PREFIX}_{current_time}{DUMP_FILE_EXTENSION}"

    print("Starting database dump process...")
    command = [
        'pg_dump',
        '-h', os.environ['DB_HOST'],
        '-p', os.environ['DB_PORT'],
        '-U', os.environ['DB_USER'],
        '-F', 'c',
        '-f', dump_file,
        os.environ['DB_NAME']
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Dump file {dump_file} created successfully.")
        if not os.path.exists(dump_file) or os.path.getsize(dump_file) == 0:
            raise Exception(f"Dump file {dump_file} was not created or is empty.")
        db.log_cron_execution(DB_DUMP_JOB_NAME, True)
        upload_to_s3(dump_file, os.environ['AWS_BUCKET_NAME'])
    except Exception as e:
        error_message = str(e)
        error_traceback = traceback.format_exc()
        db.log_cron_execution(DB_DUMP_JOB_NAME, False, error_message, error_traceback)
        print(f"An error occurred during the dump process: {error_message}")
        print(f"Error traceback: {error_traceback}")
        send_email(f"PostgresqlSnapshotManager - Database Dump Failed: {error_message}")
    finally:
        delete_old_dumps('.', days=7)

if __name__ == "__main__":
    try:
        print("Initializing database connection...")
        db = DatabaseManager()
        print("Database connection established successfully.")
    except Exception as e:
        error_message = f"Failed to establish database connection: {str(e)}"
        print(error_message)
        send_email("PostgresqlSnapshotManager - Database Connection Failed")
        raise

    try:
        main(db)
    except Exception as e:
        error_message = str(e)
        error_traceback = traceback.format_exc()
        print(f"An error occurred: {error_message}")
        db.log_cron_execution("DBDump", False, error_message, error_traceback)
        send_email("PostgresqlSnapshotManager - Database Dump Failed")
    finally:
        db.close()
        print("Database connection closed")
