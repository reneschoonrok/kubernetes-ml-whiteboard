# Dockerfile from: https://hub.docker.com/r/dtzar/helm-kubectl/dockerfile
FROM alpine:3.10

ARG VCS_REF
ARG BUILD_DATE

# Metadata
LABEL org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.name="helm-kubectl" \
      org.label-schema.url="https://hub.docker.com/r/dtzar/helm-kubectl/" \
      org.label-schema.vcs-url="https://github.com/dtzar/helm-kubectl" \
      org.label-schema.build-date=$BUILD_DATE

# Note: Latest version of kubectl may be found at:
# https://github.com/kubernetes/kubernetes/releases
ENV KUBE_LATEST_VERSION="v1.17.0"
# Note: Latest version of helm may be found at:
# https://github.com/kubernetes/helm/releases
ENV HELM_VERSION="v3.0.2"

RUN apk add --no-cache ca-certificates bash git openssh curl \
    && wget -q https://storage.googleapis.com/kubernetes-release/release/${KUBE_LATEST_VERSION}/bin/linux/amd64/kubectl -O /usr/local/bin/kubectl \
    && chmod +x /usr/local/bin/kubectl \
    && wget -q https://get.helm.sh/helm-${HELM_VERSION}-linux-amd64.tar.gz -O - | tar -xzO linux-amd64/helm > /usr/local/bin/helm \
    && chmod +x /usr/local/bin/helm

# WORKDIR /config

RUN addgroup -S appgroup && adduser -S appuser -G appgroup && apk add --update nodejs
RUN id -u appuser

RUN mkdir -p /usr/src/app/node_modules

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY public ./public/
COPY router ./router/
COPY sslcert ./sslcert/
COPY views ./views/
COPY node_modules ./node_modules/

USER 100

RUN helm repo add stable https://kubernetes-charts.storage.googleapis.com/

EXPOSE 8443
CMD [ "node", "./router/server.js" ]