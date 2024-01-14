#!/bin/sh
export DISPLAY=:0.0
BASE_PATH=$(dirname $0)
image_name=$1
caption=$2

#Push caption into caption file (overwrite)
echo $caption > $BASE_PATH/images/captions/$image_name.txt

/usr/bin/feh -ZF -K "captions" -C /usr/share/fonts/truetype/liberation/ -e LiberationSerif-Regular/96 --auto-rotate $BASE_PATH/images/$image_name



