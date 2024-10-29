FROM ubuntu:22.04

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8


RUN apt-get --yes -qq update \
 && apt-get --yes -qq upgrade \
 && apt-get --yes -qq install \
                      bzip2 \
                      cmake \
                      cpio \
                      curl \
                      g++ \
                      gcc \
                      gfortran \
                      git \
                      gosu \
                      libblas-dev \
                      liblapack-dev \
                      libopenmpi-dev \
                      openmpi-bin \
                      python3-dev \
                      python3-pip \
                      virtualenv \
                      wget \
                      zlib1g-dev \
                      vim       \
                      htop      \
                      tar \
                      libfftw3-dev \
                      openmpi-bin \
                      libopenmpi-dev \
 && apt-get --yes -qq clean \
 && rm -rf /var/lib/apt/lists/*

RUN wget https://storage.googleapis.com/gke-dja-demo_static_assets/frodock3_linux64.tgz -O frodock3_linux64.tgz

# Unpack frodock
RUN tar -xvf frodock3_linux64.tgz

# Compile frodock
WORKDIR /frodock3_linux64
RUN ./compile_frodock.sh

CMD [ "/bin/bash" ]
