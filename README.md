# PostgreSQL Snapshot Manager

This tool automates the process of creating and managing PostgreSQL database backups. It features automated dump file creation, backup retention, activity logging, email notifications on failure, and automatic upload of backups to AWS S3 for off-site storage.

## Prerequisites

- PostgreSQL
- Python 3
- `psycopg2` and `yagmail` libraries
- Access to a SMTP server (for sending emails)
- Access to an AWS account with an S3 bucket configured

## Environment Variables

Set the following environment variables before running the tool:

- `DB_NAME`: Name of the database to back up.
- `DB_USER`: Username for database authentication.
- `DB_PASS`: Password for database authentication.
- `DB_HOST`: Hostname of the database server.
- `DB_PORT`: Port on which the database server is listening.
- `GMAIL`: Gmail address to use for sending notification emails.
- `GMAILPW`: Password for the Gmail account.
- `AWS_BUCKET_NAME`: The name of the AWS S3 bucket where the dumps will be uploaded.
- `AWS_ACCESS_KEY_ID`: Your AWS access key.
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key.
- `AWS_DEFAULT_REGION`: The AWS region your S3 bucket is in.

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
```

## Uploading Backups to AWS S3

After creating a database dump, the tool will automatically upload it to the specified AWS S3 bucket. This ensures that backups are securely stored off-site and are accessible for disaster recovery purposes.

## Load the .dump file on a local Postgresql instance

The easiest way to do it is using Docker.

It is important to make sure that the docker version pulled is the same as the one where the dump file is coming from.

In the example below Postgresql:16 is used.

```
scp root@SERVER_HOST:/root/FILE_LOCATION/FILENAME.dump .
docker pull postgres:16
docker cp FILENAME.dump mypostgres16:/    
docker exec -it mypostgres16 psql -U postgres -c "CREATE DATABASE YOUR_DB_NAME;"
docker exec -it mypostgres16 pg_restore -U postgres -d YOUR_DB_NAME /FILENAME.dump     
docker exec -it mypostgres16 psql -U postgres -d YOUR_DB_NAME
```

Finally once inside the database, list all the tables available.

```
\dt
```
