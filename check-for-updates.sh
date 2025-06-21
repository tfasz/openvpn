#!/bin/bash

sudo podman pull docker.io/alpine:latest && \
        sudo podman build --no-cache -t tfasz/ovpn . && \
        sudo podman run -it --rm=true tfasz/ovpn bash -c "ovpn_genconfig vpn.example.com;ovpn_initpki;ovpn_version" > versions.txt
