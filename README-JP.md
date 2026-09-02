[English](./README.md) | 日本語

# XF_J24

[![License: OFL-1.1](https://img.shields.io/badge/License-OFL_1.1-blue.svg)](LICENSE)
[![Format](https://img.shields.io/badge/Format-OTF%20%7C%20TTF%20%7C%20WOFF2%20%7C%20BDF-brightgreen)](#)

<p align="center">
<img src="docs/24dot.svg" alt="XF_J24 フォントサンプル">
</p>

XF_J24 は [JF Dot Jiskan24 (パブリックドメイン)](http://jikasei.me/font/jf-dotfont/) をベースにした 24px のビットマップ風ゴシック体フォントです。（半角文字を除く）

Jiskan24 に含まれないグリフ（文字）については、[Source Han Sans (OFL 1.1)](https://github.com/adobe-fonts/source-han-sans) および [Inter (OFL 1.1)](https://github.com/rsms/inter) のデザインをベースに補完しています。

## ダウンロード / インストール

コンパイル済みのフォントファイル（`.otf`、`.ttf`、`.woff2`）は [Releases](https://github.com/akashiyaki01c/XF_J24/releases) ページからダウンロードできます。

1. [Releases](https://github.com/akashiyaki01c/XF_J24/releases/latest) にアクセスし、最新のフォントファイルをダウンロードします。
2. OS に `.ttf` または `.otf` ファイルをインストールします（Webフォントとして使用する場合は、CSSの `@font-face` ルールで `.woff2` を指定してください）。

## 収録文字

このフォントには、JIS第1水準およびJIS第2水準の漢字セットが含まれています。

> **Note:** 一部のグリフは現在も手作業によるデザイン調整や修正を行っています。

## ライセンス

このフォントは [SIL Open Font License 1.1](LICENSE) のもとでライセンスされています。
商用利用・個人利用を問わず、ご自由にお使いいただけます。

### 謝辞とライセンス表記

XF_J24 は、以下のオープンソースプロジェクトをベースにして構築、およびデザインを取り入れています：

- **[JF Dot Jiskan24 (全角文字のみ)](http://jikasei.me/font/jf-dotfont/)**: パブリックドメイン
- **[Source Han Sans](https://github.com/adobe-fonts/source-han-sans)**: [SIL Open Font License 1.1](https://scripts.sil.org/OFL) (© 2014-2021 Adobe)
- **[Inter](https://github.com/rsms/inter)**: [SIL Open Font License 1.1](https://scripts.sil.org/OFL) (© 2016-2020 Rasmus Andersson)

## リポジトリ構造

- `XF_J24.kbitx`: Bits'N'Picas ソースファイル
- `fonts/`: コンパイル済みフォントファイル (`.otf`, `.ttf`, `.woff2`)

## 開発 / ソースからのビルド

システムに [Bits'N'Picas](https://github.com/pjb108/BitsNPicas) および [FontForge](https://fontforge.org/) がインストールされている必要があります。

```bash
# fonts/ ディレクトリに .otf、.ttf、および .woff2 を生成します
bash build.sh