#!/bin/bash

docker run \
  --name ahome-rabbit \
  -p 15672:15672 \
  -p 25672:25672 \
  -p 4369:4369 \
  -p 5671:5671 \
  -p 5672:5672 \
  -d ahome_rabbit

