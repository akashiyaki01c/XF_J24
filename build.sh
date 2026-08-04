#!/usr/bin/env bash

set -euo pipefail

SRC_KBITX="./XF_J24.kbitx"
SRC_SFDIR="./XF_Nstf.sfdir"
OUT_DIR="fonts"

mkdir -p "${OUT_DIR}"

echo "🔨 Building fonts from ${SRC_KBITX}..."

# java -jar /Applications/BitsNPicas.jar convertbitmap -o "${OUT_DIR}/XF_J24_base.ttf" -f ttf "${SRC_KBITX}"

echo "🔨 Building fonts from ${SRC_SFDIR}..."

fontforge -lang=py -c "
import fontforge, sys

sfdir_path = sys.argv[1]
out_dir = sys.argv[2]

print('  -> Loading ttf...')
font = fontforge.open(sfdir_path)

print('  -> Generating OTF...')
font.generate(f'{out_dir}/XF_J24.otf')

print('  -> Generating TTF...')
font.generate(f'{out_dir}/XF_J24.ttf')

print('  -> Generating WOFF2...')
font.generate(f'{out_dir}/XF_J24.woff2')

font.close()

print('  -> Scaling to 26px equivalent...')
font_26 = fontforge.open(sfdir_path)
scale_factor = 24.0 / 26.0
em = font_26.em
for g in font_26.glyphs():
    if g.unicode >= 0 or g.glyphname:
        orig_width = g.width
        offset_x = (orig_width * (1.0 - scale_factor)) / 2.0
        offset_y = (em * (1.0 - scale_factor)) / 2.0

        mat = psMat.compose(psMat.scale(scale_factor), psMat.translate(offset_x, offset_y))
        g.transform(mat)

        g.round()

        g.width = orig_width

font_26.familyname = font_26.familyname + '_26'
font_26.fontname = font_26.fontname + '_26'
font_26.fullname = font_26.fullname + '_26'

print('  -> Generating 26px Padded (.otf, .ttf)...')
font_26.generate(f'{out_dir}/XF_J24_26.otf')
font_26.generate(f'{out_dir}/XF_J24_26.ttf')
font_26.generate(f'{out_dir}/XF_J24_26.woff2')
font_26.close()

" "${OUT_DIR}/XF_J24_base.ttf" "${OUT_DIR}"

echo "Build complete! Output files are in ${OUT_DIR}/"
