FROM postgres:17-bookworm

RUN apt-get update && \
    apt-get install -y curl unzip && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip" && \
    unzip /tmp/awscliv2.zip -d /tmp && \
    /tmp/aws/install && \
    rm -rf /var/lib/apt/lists/* /tmp/*

ENV BACKUP_FILE=/tmp/db_backup.sql.gz

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["
  echo 'Starting pg_dump...';
  PGPASSWORD=$POSTGRES_PASSWORD pg_dump -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DATABASE | gzip > $BACKUP_FILE;
  echo 'Uploading to S3...';
  aws --endpoint-url http://$S3_ENDPOINT s3 cp $BACKUP_FILE s3://$S3_BUCKET/$S3_PREFIX/db_backup_$(date +%s).sql.gz
"]
