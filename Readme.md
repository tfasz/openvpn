
# OpenVPN Docker Container

This project was inspired by https://github.com/kylemanna/docker-openvpn but intends to provide regular updates.
As of October 2022, this project's image was running a two year old version of OpenVPN.
```
docker run -it --rm=true --pull=always kylemanna/openvpn openvpn --version
...
OpenVPN 2.4.9 x86_64-alpine-linux-musl [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [MH/PKTINFO] [AEAD] built on Apr 20 2020
library versions: OpenSSL 1.1.1g  21 Apr 2020, LZO 2.1
...
```

This project also simplifies and provides secure by default OpenVPN configuration. This takes input from
some other projects and blog posts including:
* https://github.com/Angristan/OpenVPN-install
* https://polansky.co/blog/hardening-openvpn-in-2020/

General security improvements include:
* use ECDSA certificates with prime256v1 curve
* require a minimum of TLS version 1.2
* use tls-crypt to authenticate tcp control channel packets
* authenticate packets with `SHA256`
* use modern `AES-128-GCM` cipher for data channel
* verify server x509 certificate name matches VPN common name

Feel free to suggest corrections, improvements, etc.

# Getting Started

This guide will show you how to use docker-compose to configure and run your OpenVPN container.

## Configure and Start OpenVPN Server Container
1. Ensure you have Docker and docker-compose installed and working.
2. Create a directory to manage your VPN server config.
3. Copy the `docker-compose.yml` file from this project your directory.
4. Generate your OpenVPN server.conf configuration by running (see examples below):

       docker-compose run --rm openvpn ovpn_genconfig ...

5. Initalize your PKI to create your CA and server keys:

       docker-compose run --rm openvpn ovpn_initpki

6. Start your openvpn container with `docker-compose up -d` and review startup logs with `docker logs -f openvpn`.

### Server Configuration Options

You can view server configuration options by running:

       docker-compose run --rm openvpn ovpn_genconfig --help

#### Examples

* listen on UDP port 1194 for the host `vpn.example.com` with DNS 8.8.8.8:

       `docker-compose run --rm openvpn ovpn_genconfig -d 8.8.8.8 vpn.example.com`

* listen on TCP port 1194 for the host `vpn.example.com` with DNS 8.8.8.8 and 8.8.4.4:

      docker-compose run --rm openvpn ovpn_genconfig -t -d 8.8.8.8 -d 8.8.4.4 vpn.example.com

* listen on TCP port 443 for the host `vpn.example.com` with DNS 192.168.0.2:

      docker-compose run --rm openvpn ovpn_genconfig -t -p 443 -d 192.168.0.2 vpn.example.com

* add notification to a Slack webhook for logging client connect/disconnect events (see below for more details)

      docker-compose run --rm openvpn ovpn_genconfig ... -s https://hooks.slack.com/...

## Generate Client Config

Once your server is configurd you can generate one or more client configurations.

1. Create your client and save the client configuration with:

       docker-compose run --rm openvpn ovpn_getclient [CLIENT-NAME] > client.ovpn

This will create the client certificate if it does not yet exist and then output the config file
which can be used by the client to setup the VPN config. If the client already exists it will just
output the config file.

## Revoke Client Config

You can revoke a client certificate by running:

       docker-compose run --rm openvpn ovpn_revokeclient [CLIENT-NAME]

## Slack Notifications

You can configure OpenVPN to call a script on client connect/disconnect. An example of a script which posts
notifications to Slack is included. You will first need to set up a Slack Webhook integration following [their
documentation](https://slack.com/help/articles/115005265063-Incoming-webhooks-for-Slack)
and then include the Webhook URL when configuring the server.

## Backup Data Directory

Your PKI and configuration files will be written to the `data` directory. You should securely backup this folder
to ensure it is not lost in the case of a hard drive failure.

# Build and Release Process

## Building and Testing Locally

The [Dockerfile](Dockerfile) is a multi-stage build which will create a base container image, run
the tests and linting, and then create a final container with the config. This allows you to build the
image, run tests and linting, and create a container image with:

       docker build -t openvpn .

## Check Latest Versions

To check and see if there are version updates available. The `versions.txt` file will be updated if there are any available.

       docker pull alpine:latest && docker build --no-cache -t openvpn . && docker run -it ovpn ovpn_version > versions.txt

## Releases

Releases are tagged with the current year, month, and an incrementing release number.

1. Tag release on `main` branch: `git tag <YYYY-MM-NUM> && git push --tags`
2. Create release via GitHub UI from tag.

This will build and publish a Docker container tagged with that version: `docker pull ghcr.io/tfasz/openvpn:TAG`
