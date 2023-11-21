#!/bin/sh

set -e

echo "creating exe..."
pyinstaller teethpack.py --onefile --strip --noupx
echo "packing..."
tar --owner=0 --group=0 -czvf dist/teethpack.tar.gz \
    README \
    LICENSE \
    teethpack.sh \
    dist/teethpack \
    drophere/info.txt \
    output/info.txt
echo "done."
