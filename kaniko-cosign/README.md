# kaniko

This container is based off of [kaniko](https://github.com/GoogleContainerTools/kaniko) but sources other containers.

* [cosign](https://github.com/sigstore/cosign)
* [vault](https://hub.docker.com/r/hashicorp/vault)

It is used by a pipelines to build and sign container images.

## CHANGELOG

* 2025.05.23 - Initial image