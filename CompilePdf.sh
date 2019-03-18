#!/bin/bash

function msg {
  echo $@ >&2
}

if ! [ -d "$1" ]
then
  msg "Please, provide a directory with SVGs: $0 OUT-DIR"
  exit 1
fi
DIR=`basename $1`

if ! [ -x "$(command -v pdftk)" ]; then
  msg 'Error: pdftk is not installed.'
  msg "Either 16.04 sudo apt-get install pdftk OR on 18.04 sudo snap install pdftk"
  exit 2
fi

if ! [ -x "$(command -v convert)" ]; then
  msg 'Error: ImageMagick is not installed.'
  msg "sudo apt-get install imagemagick"
  exit 3
fi


res=`grep "PDF" /etc/ImageMagick-6/policy.xml | grep "none" | wc -l`
if [ "$res" -gt 0 ]
then
  msg "Please, enable PDF writing replacing 'none' for 'write' in /etc/ImageMagick-6/policy.xml"
  msg ' Like this:       <policy domain="coder" rights="write" pattern="PDF" />'
  exit 4
fi

echo "Processing $DIR"

cd $DIR

for f in *.svg
do
  msg "Converting $f to PDF"
  convert -density 300 $f -quality 100 $f.pdf
  if [[ $? != 0 ]]; then exit 5; fi
done

msg "Making a single PDF ..."

rm Compiled.pdf 2>/dev/null

pdftk *.pdf cat output Compiled.pdf
msg "Cleanup..."
rm -rf *.svg.pdf
msg "Done!"
msg "Check result: evince "`readlink -f Compiled.pdf`
msg ""



