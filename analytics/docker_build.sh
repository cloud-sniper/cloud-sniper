#!/usr/bin

DEFAULT_IMAGE_NAME=cloudsniper/beaconer

usage()
{
    echo "Usage: docker_build.sh [image_name]"
    echo "\timage_name is optional (default "$DEFAULT_IMAGE_NAME")"
}

case $1 in
    -h | --help )
    usage
    exit 0
esac

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo "Building the docker image with Dockerfile defined at $SCRIPTPATH"

if [ "$#" -ge 2 ]; then
    usage
fi

IMAGE_NAME=${DEFAULT_IMAGE_NAME}
if [ "$#" -eq 1 ]; then
    IMAGE_NAME=$1
fi

echo docker build $SCRIPTPATH -t $IMAGE_NAME
docker build $SCRIPTPATH -t $IMAGE_NAME
