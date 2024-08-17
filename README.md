## 概要

- https://github.com/ikin5050/osuAnonmap#osuanonmap のフォークリポジトリです。
  <br>ツール自体の説明は本家を確認してください。
- ~~本リポジトリでは上記ツールを Re:TJBC 向けに書き換えています。~~
  本ブランチ `for-single-osz` は、個人の利用(コラボやコンテスト)向けに更に修正を加えたものになります。
  - whisle -> clap
  - editor上の通常ノーツを全て中央へ移動
  - その他editor情報の匿名化(GridSize, BeatDivisor等)

## 実行方法

1. `python main.py <変換したいoszのパス>` を実行
2. `output/` 以下に配置される osz ファイルを確認
