# Stage 1: Borrow from TensorChord's pgvecto.rs PG17 image
FROM tensorchord/pgvecto-rs:pg17-nightly as pgvecto

# Stage 2: Your actual runtime image (CloudNativePG official)
FROM ghcr.io/cloudnative-pg/postgresql:17.5

USER root

# Install contrib if you want to be extra sure cube/earthdistance exist
RUN apt-get update && \
    apt-get install -y postgresql-contrib && \
    rm -rf /var/lib/apt/lists/*

# Copy pgvecto.rs extension files from the first stage
COPY --from=pgvecto /usr/lib/postgresql/17/lib/pgvecto_rs.so /usr/lib/postgresql/17/lib/
COPY --from=pgvecto /usr/share/postgresql/17/extension/pgvecto_rs.control /usr/share/postgresql/17/extension/
COPY --from=pgvecto /usr/share/postgresql/17/extension/vectors--*.sql /usr/share/postgresql/17/extension/

USER 26