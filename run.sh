#!/usr/bin/bash

IMAGE_NAME="my_scanner:0.1"

docker build -t "$IMAGE_NAME" .

docker run -e GITHUB_TOKEN "$IMAGE_NAME"
