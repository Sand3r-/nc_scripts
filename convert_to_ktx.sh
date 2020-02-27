#!/bin/bash
cd output
FILES=./*
for f in $FILES
do
  echo "Processing $f file..."
  EtcTool.exe ./$f -format RGB8A1 -effort 100 -output ./"${f%.*}.ktx"
  rm $f
done