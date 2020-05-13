#!/bin/bash

docker run \
  --name ahome-webssh \
  -p 9001:9001 \
  -p 7000:7000 \
  -v /opt/tmp:/opt/tmp \
  -d ahome_webssh