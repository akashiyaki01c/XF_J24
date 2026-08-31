#!/usr/bin/env bash

SRC_KBITX="./XF_J24.kbitx"
SRC_SFDIR="./XF_Nstf.sfdir"
OUT_DIR="fonts"

mkdir -p "${OUT_DIR}"

echo "Building fonts from ${SRC_KBITX}..."

java -jar /Applications/BitsNPicas.jar convertbitmap -o "${OUT_DIR}/XF_J24_base.bdf" -f bdf "${SRC_KBITX}"

fontforge -lang=py dot.py "${OUT_DIR}/XF_J24_base.bdf" fonts/
