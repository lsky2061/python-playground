#!/bin/sh
export DISPLAY=:0.0
BASE_PATH=$(dirname $0)

/usr/bin/feh -ZF -K "captions" -C /usr/share/fonts/truetype/liberation/ -e LiberationSerif-Regular/96 --auto-rotate $BASE_PATH/images/test_image.png



