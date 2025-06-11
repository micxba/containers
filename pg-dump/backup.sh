#!/bin/bash
set -e

echo "Starting pg_dump..."
env
export BACKUP_FILE=/tmp/${POSTGRES_DATABASE}_backup.sql.gz
PGPASSWORD="$POSTGRES_PASSWORD" pg_dump -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DATABASE" | gzip > "$BACKUP_FILE"

echo "Uploading to S3..."
aws --endpoint-url "http://$S3_ENDPOINT" s3 cp "$BACKUP_FILE" "s3://$S3_BUCKET/$S3_PREFIX/db_backup_$(date +%s).sql.gz"
