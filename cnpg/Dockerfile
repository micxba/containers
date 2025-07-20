FROM ghcr.io/cloudnative-pg/postgresql:17.5

USER root

# Install contrib extensions (if needed)
RUN apt-get update && \
    apt-get install -y postgresql-contrib && \
    rm -rf /var/lib/apt/lists/*

# Install pgvecto.rs
ADD https://github.com/tensorchord/pgvecto.rs/releases/download/v0.2.0/pgvecto_rs-pg17.deb /tmp/
RUN dpkg -i /tmp/pgvecto_rs-pg17.deb && rm /tmp/pgvecto_rs-pg17.deb

# Return to the default non-root user for security (Postgres images run as postgres user)
USER 26