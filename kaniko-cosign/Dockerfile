ARG COSIGN_VERSION=v2.4.3
ARG VAULT_VERSION=1.18.1
ARG KANIKO_VERSION=v1.23.2-debug

FROM ghcr.io/sigstore/cosign/cosign:$COSIGN_VERSION AS cosign
FROM hashicorp/vault:$VAULT_VERSION AS vault
FROM gcr.io/kaniko-project/executor:$KANIKO_VERSION

COPY --from=cosign /ko-app/cosign /usr/local/bin/cosign
COPY --from=vault /bin/vault /usr/local/bin/vault

LABEL org.opencontainers.image.authors="sith.network"