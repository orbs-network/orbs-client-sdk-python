FROM debian:stretch

RUN apt-get update && apt-get install -y python-dev libboost-python-dev python-pip build-essential curl

RUN curl https://cmake.org/files/v3.10/cmake-3.10.2-Linux-x86_64.sh --output cmake-bootstrap && \
    bash cmake-bootstrap --skip-license --prefix=/usr && rm cmake-bootstrap

ADD . /opt/orbs-sdk

WORKDIR /opt/orbs-sdk

RUN ./download-crypto-sdk.sh

RUN ./build.sh
