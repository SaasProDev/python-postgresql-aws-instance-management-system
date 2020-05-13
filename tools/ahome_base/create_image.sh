#!/bin/bash

docker build -f Dockerfile.prebase -t ahome_prebase . && \
docker build -f Dockerfile.pyton37 -t ahome_pyton37 . && \
docker build -f Dockerfile.base -t ahome_base .
