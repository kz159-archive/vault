#!/usr/bin/env bash

set -ex

VERSION=$(date +%Y-%m-%d)
IMGNAME=capturica/vault
REGNAME=registry.dev.mrbot.im
GITBRANCH=$(git rev-parse --abbrev-ref HEAD)

docker build -t ${IMGNAME} .
docker tag $IMGNAME $REGNAME/$IMGNAME:$VERSION-$GITBRANCH
docker tag $IMGNAME $REGNAME/$IMGNAME:latest
if [[ -n $1 ]]; then
    docker push $REGNAME/$IMGNAME:$VERSION-$GITBRANCH
    docker push $REGNAME/$IMGNAME:latest
fi

echo "docker register sync done"
echo "current version is \`docker pull $REGNAME/$IMGNAME:$VERSION-$GITBRANCH\`"