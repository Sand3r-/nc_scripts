#!/bin/bash
cd output
FILES=./*
for f in $FILES
do
  if [[ $f != *".ktx"* ]]; then
    echo "Processing $f file..."
    EtcTool.exe ./$f -format RGB8A1 -m 7 -effort 100 -output ./"${f%.*}.ktx"
    rm $f
  fi
done