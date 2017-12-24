#!/bin/bash


for image in original-icons/*.png
do
    name=${image##*/}
    convert $image -fuzz 0.5% -trim +repage -resize 30x30\> -sharpen 0x1.4 -background none -gravity center -extent 30x30 resized.png
    convert resized.png -channel A -virtual-pixel transparent -morphology EdgeOut Diamond outside.png
    convert outside.png -threshold 100% outline.png
    convert resized.png outline.png -compose Over -composite icons/$name 
    echo $name moving to icons/$name
    rm resized.png outside.png outline.png
done

#convert original-icons/1.png -fuzz 0.5% -trim +repage -resize 30x30\> -sharpen 0x1.4 -background none -gravity center -extent 30x30 1_resize.png
#convert 1_resize.png -channel A -virtual-pixel transparent -morphology EdgeOut Diamond 1_out.png
#convert 1_resize.png 1_out_black.png -compose Over -composite 1_resize_outline.png

#eog 1_resize_border.png &
