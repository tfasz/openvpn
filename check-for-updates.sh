#!/bin/bash

docker pull alpine:latest && \
        docker build --no-cache -t tfasz/ovpn . && \
        docker run -it --rm=true tfasz/ovpn bash -c "ovpn_genconfig vpn.example.com;ovpn_initpki;ovpn_version" > versions.txt
