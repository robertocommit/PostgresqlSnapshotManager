# PostgreSQL Snapshot Manager

This tool automates the process of creating and managing PostgreSQL database backups. It features automated dump file creation, backup retention, activity logging, and email notifications on failure.

## Prerequisites

- PostgreSQL
- Python 3
- `psycopg2` and `yagmail` libraries
- Access to a SMTP server (for sending emails)

## Environment Variables

Set the following environment variables before running the tool:

- `DB_NAME`: Name of the database to back up.
- `DB_USER`: Username for database authentication.
- `DB_PASS`: Password for database authentication.
- `DB_HOST`: Hostname of the database server.
- `DB_PORT`: Port on which the database server is listening.
- `GMAIL`: Gmail address to use for sending notification emails.
- `GMAILPW`: Password for the Gmail account.

## Database Log Table

Create a table in your PostgreSQL database to store logs:

```sql
CREATE TABLE cron_job_log (
    job_name TEXT,
    status BOOLEAN,
    error_message TEXT,
    error_traceback TEXT,
    execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
