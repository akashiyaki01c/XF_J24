#!/usr/bin/env fontforge -lang=py
# -*- coding: utf-8 -*-

import sys
import os
import math
import fontforge
import psMat

# ==========================================
# 設定パラメータ
# ==========================================
# 1ドット（ピクセル）に対する「丸」の大きさの割合 (0.0 〜 1.0)
# 0.8  : ドット同士に適度な隙間ができる（電光掲示板・LED掲示板風）
# 1.0  : 正方形に内接する直径（隣の丸とギリギリ接触する）
# 1.15 : ドット同士が少し重なって密着感が出る
DOT_SCALE = 0.8

# フォントの設定
EM_SIZE = 1000        # UPM (Units Per Em)
FONT_NAME = "XF_J24-Dot"
FULL_NAME = "XF_J24 Dot"
FAMILY_NAME = "XF_J24 Dot"

# ==========================================
# 補助関数: 円（丸ドット）の描画
# ==========================================
def draw_circle(pen, cx, cy, r):
    """
    指定した中心 (cx, cy) と半径 r の円（ベクターパス）を描画する。
    FontForge の 3次ベジェ曲線による真円近似 (k ≒ 0.5522847) を使用。
    """
    k = r * 0.552284749831

    pen.moveTo((cx + r, cy))
    pen.curveTo((cx + r, cy + k), (cx + k, cy + r), (cx, cy + r))
    pen.curveTo((cx - k, cy + r), (cx - r, cy + k), (cx - r, cy))
    pen.curveTo((cx - r, cy - k), (cx - k, cy - r), (cx, cy - r))
    pen.curveTo((cx + k, cy - r), (cx + r, cy - k), (cx + r, cy))
    pen.closePath()

# ==========================================
# BDF パース関数
# ==========================================
def parse_bdf(bdf_path):
    """
    BDFファイルを読み込み、各文字のビットマップ配列 (2Dリスト) を返す。
    戻り値: { encoding (int): {'bbx': (w, h, xoff, yoff), 'bitmap': [[0/1, ...], ...]} }
    """
    glyphs = {}
    current_encoding = None
    current_bbx = None
    bitmap_lines = []
    in_bitmap = False

    with open(bdf_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            cmd = parts[0]

            if cmd == 'ENCODING':
                current_encoding = int(parts[1])
            elif cmd == 'BBX':
                # BBX width height xoff yoff
                current_bbx = (int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]))
            elif cmd == 'BITMAP':
                in_bitmap = True
                bitmap_lines = []
            elif cmd == 'ENDCHAR':
                in_bitmap = False
                if current_encoding is not None and current_bbx is not None:
                    bw, bh, xoff, yoff = current_bbx
                    grid = []
                    for hex_str in bitmap_lines:
                        # 16進数を2進数文字列に変換 (桁数を合わせる)
                        val = int(hex_str, 16)
                        bits_str = bin(val)[2:].zfill(len(hex_str) * 4)
                        # BBXの幅分だけ取り出して 0/1 の数値リストにする
                        row = [int(b) for b in bits_str[:bw]]
                        grid.append(row)
                    
                    glyphs[current_encoding] = {
                        'bbx': current_bbx,
                        'bitmap': grid
                    }
                current_encoding = None
                current_bbx = None
            elif in_bitmap:
                bitmap_lines.append(line)

    return glyphs

# ==========================================
# メイン処理
# ==========================================
def main():
    if len(sys.argv) < 3:
        print("Usage: fontforge -lang=py generate_dot_font.py <input.bdf> <output_dir>")
        sys.exit(1)

    bdf_path = sys.argv[1]
    out_dir = sys.argv[2]

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    print(f"Parsing BDF file: {bdf_path}...")
    bdf_data = parse_bdf(bdf_path)
    print(f"  -> Found {len(bdf_data)} glyphs.")

    # 1. 新しい空のフォントを作成
    font = fontforge.font()
    font.em = EM_SIZE
    font.fontname = FONT_NAME
    font.fullname = FULL_NAME
    font.familyname = FAMILY_NAME

    # 24×24 を前提として、1ピクセルのグリッドサイズを計算
    # (ここでは 24×24 ピクセルで EM_SIZE(1000) を覆う想定)
    GRID_SIZE = 24
    px_unit = EM_SIZE / float(GRID_SIZE)  # 1px ≒ 41.667 units
    radius = (px_unit * DOT_SCALE) / 2.0

    print("Generating vector dots...")
    for unicode_val, data in bdf_data.items():
        if unicode_val < 0:
            continue

        # グリフ作成
        g = font.createChar(unicode_val)
        bbx_w, bbx_h, xoff, yoff = data['bbx']
        bitmap = data['bitmap']

        pen = g.glyphPen()

        # BDFのY軸は上から下、FontForgeのY軸は下から上（ベースライン基準）
        # 24pxのグリッド内で上揃え〜ベースライン位置へ配置
        for y_idx, row in enumerate(bitmap):
            for x_idx, bit in enumerate(row):
                if bit == 1:
                    # ピクセルの中心座標 (FontForgeのベクター空間) を計算
                    # ※ y軸は BDF(上原点) から FontForge(下原点) へ反転
                    pixel_x = xoff + x_idx
                    pixel_y = (GRID_SIZE - 1) - (y_idx - yoff)

                    center_x = (pixel_x + 0.5) * px_unit
                    center_y = (pixel_y + 0.5) * px_unit

                    # 丸を描画
                    draw_circle(pen, center_x, center_y, radius)

        # パスの向きを自動補正（塗りつぶし・抜きの方向を正しくする）
        g.correctDirection()
        
        # 座標を整数値に丸めてキレイにする
        g.round()

        # 文字幅（アバンス）の設定 (全角=EM_SIZE, 半角=EM_SIZE/2)
        if bbx_w <= 12:
            g.width = int(EM_SIZE / 2)
        else:
            g.width = EM_SIZE

    # 2. ファイル書き出し
    otf_path = os.path.join(out_dir, f"{FONT_NAME}.otf")
    ttf_path = os.path.join(out_dir, f"{FONT_NAME}.ttf")

    print(f"Exporting {otf_path}...")
    font.generate(otf_path)

    print(f"Exporting {ttf_path}...")
    font.generate(ttf_path)

    font.close()
    print("Build complete!")

if __name__ == "__main__":
    main()