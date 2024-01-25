# Original credit: https://github.com/jpetazzo/dockvpn
FROM alpine:latest as base
LABEL maintainer="tfasz"

# Setup /opt/ovpn folder for all of our config scripts. We will later symlink shortcuts to this location.
ADD ./requirements.txt /opt/
RUN apk add --update openvpn iptables bash easy-rsa python3 && \
    rm /usr/lib/python3.11/EXTERNALLY-MANAGED && \
    python3 -m ensurepip && pip3 install --no-cache --upgrade pip setuptools && \
    pip3 install -r /opt/requirements.txt && \
    ln -s /usr/share/easy-rsa/easyrsa /usr/local/bin && \
    rm -rf /tmp/* /var/tmp/* /var/cache/apk/* /var/cache/distfiles/*

# Set our ENV vars, working directory, exposed port, and scripts
ENV OPENVPN=/etc/openvpn
ENV EASYRSA=/usr/share/easy-rsa \
    EASYRSA_PKI=$OPENVPN/pki \
    EASYRSA_VARS_FILE=$OPENVPN/pki/vars
WORKDIR /etc/openvpn
EXPOSE 1194/udp

# Use a multi-stage build to run tests and lint in this same container.
# You can build image with test dependencies + code: docker build -t ovpn-test --target test-base .
# You can build and run tests with: docker build -t ovpn-test --target test .
FROM base as test-base

# Install requirements first so we don't need to do this everytime our scripts/tests change.
ADD ./requirements-test.txt /opt/
RUN pip3 install -r /opt/requirements-test.txt
# Copy whole directory and run tests + lint
ADD . /opt/ovpn-test
FROM test-base as test
RUN cd /opt/ovpn-test && pytest -vv --cov=ovpn/ --cov-fail-under=98 --cov-report term-missing && \
    pylint ovpn/*.py tests/*.py

# If we pass our tests and lint create a container without the tests/lint libs + code.
FROM base as default
ADD ./ovpn /opt/ovpn
RUN ln -s /opt/ovpn/ovpn_genconfig.py /usr/local/bin/ovpn_genconfig && \
    ln -s /opt/ovpn/ovpn_initpki.py /usr/local/bin/ovpn_initpki && \
    ln -s /opt/ovpn/ovpn_getclient.py /usr/local/bin/ovpn_getclient && \
    ln -s /opt/ovpn/ovpn_notify.py /usr/local/bin/ovpn_notify && \
    ln -s /opt/ovpn/ovpn_revokeclient.py /usr/local/bin/ovpn_revokeclient && \
    ln -s /opt/ovpn/ovpn_run /usr/local/bin/ovpn_run && \
    ln -s /opt/ovpn/ovpn_version /usr/local/bin/ovpn_version && \
    chmod a+x /opt/ovpn/ovpn_run /opt/ovpn/ovpn_version /opt/ovpn/*.py
CMD ["ovpn_run"]
