#!/bin/bash

function outline {
    convert $1 -channel A -virtual-pixel transparent -morphology EdgeOut Diamond outside.png
    convert outside.png -threshold 100% outline.png
    convert $1 outline.png -compose Over -composite $2
    rm outside.png outline.png
}

function workon {
    name=${1##*/}
    convert $1 -fuzz 0.5% -trim +repage -resize 30x30\> -sharpen 0x1.4 -background none -gravity center -extent 30x30 icon.png
    convert $1 -fuzz 0.5% -trim +repage -resize 94x94\> -sharpen 0x1.4 -background none -gravity center -extent 94x94 larger.png
    outline icon.png icon-outlined.png 
    outline larger.png larger-outlined.png
    rm icon.png larger.png
    mv icon-outlined.png icons/$name
    mv larger-outlined.png larger-icons/$name
}

if [ $# -eq 0 ]; then
    for image in original-icons/*.png
    do
        workon $image
    done
    exit 0
elif [ $# -eq 1 ]; then 
    workon $1
    exit 0
fi

exit 0

