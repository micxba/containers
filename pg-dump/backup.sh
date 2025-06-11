#!/bin/bash
set -e

export AWS_ACCESS_KEY_ID="$S3_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="$S3_SECRET_ACCESS_KEY"
export BACKUP_FILE=/tmp/db_backup.sql.gz

echo "Starting pg_dump..."
PGPASSWORD="$POSTGRES_PASSWORD" pg_dump -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DATABASE" | gzip > "$BACKUP_FILE"

echo "Uploading to S3..."
aws --endpoint-url "http://$S3_ENDPOINT" s3 cp "$BACKUP_FILE" "s3://$S3_BUCKET/$S3_PREFIX/db_backup_$(date +%s).sql.gz"
