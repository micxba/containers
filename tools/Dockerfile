FROM rockylinux/rockylinux:9-minimal

RUN microdnf -y update && microdnf -y install \
  openssh-clients \
  python3.12-pip \
  sudo \
  tar \
  unzip \
  && microdnf clean all

RUN pip3.12 install \
  ansible==9.10.0 \
  cryptography==42.0.8 \
  oci-cli \
  requests \
  && pip3.12 cache purge

RUN curl -sL https://talos.dev/install | sh

RUN AWSCLI_VERSION=2.22.24 && curl -s -o awscliv2.zip https://awscli.amazonaws.com/awscli-exe-linux-x86_64-${AWSCLI_VERSION}.zip && \
  unzip -q awscliv2.zip && \
  ./aws/install && \
  rm -rf ./aws && \
  rm -f ./awscliv2.zip

# Set desired Vault version
ENV VAULT_VERSION=1.18.1

# Download and install Vault CLI
RUN curl -Lo /tmp/vault.zip https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_amd64.zip && \
    unzip /tmp/vault.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/vault && \
    rm -f /tmp/vault.zip


RUN curl -sL "https://github.com/mikefarah/yq/releases/download/v4.45.1/yq_linux_amd64" -o /usr/local/bin/yq
RUN chmod +x /usr/local/bin/yq

LABEL org.opencontainers.image.authors="sith.network"
LABEL org.opencontainers.image.source https://github.com/micxba/containers
