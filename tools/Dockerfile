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

LABEL org.opencontainers.image.authors="sith.network"
