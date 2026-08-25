#!/usr/bin/env bash

set -euo pipefail

# 1. Setting Property
FONT_FAMILY="XF_J24"
FONT_NAME="XF_J24-Regular"     # PostScript Name
FONT_STYLE="Regular"           # Style Name
VERSION="1.0.0-beta.1"         # Release Version
FONT_VER_NUM="0.900"           # Internal Version (Numeric)

SRC_KBITX="./XF_J24.kbitx"
OUT_DIR="fonts"
BASE_TTF="${OUT_DIR}/XF_J24_base.ttf"

IS_RELEASE="false"
while [[ $# -gt 0 ]]; do
  case "$1" in
    -r|--release)
      IS_RELEASE="true"
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# 2. Build Command
mkdir -p "${OUT_DIR}"

echo "Building base bitmap TTF from ${SRC_KBITX}..."
rm "${BASE_TTF}"
java -jar /Applications/BitsNPicas.jar convertbitmap -o "${BASE_TTF}" -f ttf "${SRC_KBITX}"

echo "Processing font with FontForge..."

fontforge -lang=py -script - \
  "${BASE_TTF}" \
  "${OUT_DIR}" \
  "${FONT_NAME}" \
  "${FONT_FAMILY}" \
  "${FONT_STYLE}" \
  "${VERSION}" \
  "${FONT_VER_NUM}" \
  "${IS_RELEASE}" <<'EOF'
import fontforge, sys

# args
base_ttf_path = sys.argv[1]
out_dir       = sys.argv[2]
font_name     = sys.argv[3]
font_family   = sys.argv[4]
font_style    = sys.argv[5]
version_str   = sys.argv[6]
ver_num       = sys.argv[7]
is_release    = sys.argv[8] == "true"

full_name = f"{font_family} {font_style}"

print(f"  -> Loading base font from {base_ttf_path}...")
font = fontforge.open(base_ttf_path)

# metadata
font.fontname   = font_name
font.familyname = font_family
font.fullname   = full_name
font.version    = ver_num

# OpenType Name Table
font.appendSFNTName('English (US)', 'Family', font_family)
font.appendSFNTName('English (US)', 'SubFamily', font_style)
font.appendSFNTName('English (US)', 'Fullname', full_name)
font.appendSFNTName('English (US)', 'Version', f'Version {version_str}')

# --- export ---
if is_release:
    file_prefix = f"{out_dir}/{font_name}-{version_str}"
else:
    file_prefix = f"{out_dir}/{font_name}"

print(f"  -> Generating OTF: {file_prefix}.otf")
font.generate(f"{file_prefix}.otf")

print(f"  -> Generating TTF: {file_prefix}.ttf")
font.generate(f"{file_prefix}.ttf")

print(f"  -> Generating WOFF2: {file_prefix}.woff2")
font.generate(f"{file_prefix}.woff2")

font.close()
EOF

echo "Build complete! Output files are in ${OUT_DIR}/"