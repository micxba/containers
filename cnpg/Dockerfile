FROM ghcr.io/cloudnative-pg/postgresql:17.5

# Install contrib extensions (if not already present)
RUN apt-get update && \
    apt-get install -y postgresql-contrib && \
    rm -rf /var/lib/apt/lists/*

# Install pgvecto.rs extension (adjust version as needed)
# Get the .deb package from https://github.com/tensorchord/pgvecto.rs/releases
ADD https://github.com/tensorchord/pgvecto.rs/releases/download/v0.2.0/pgvecto_rs-pg17.deb /tmp/
RUN dpkg -i /tmp/pgvecto_rs-pg17.deb && rm /tmp/pgvecto_rs-pg17.deb

# (Optional) Show installed extensions for verification
RUN ls -l /usr/lib/postgresql/17/lib/ | grep pgvecto
RUN ls -l /usr/share/postgresql/17/extension/ | grep pgvecto