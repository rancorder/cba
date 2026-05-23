# CBA 商談プレゼン 完全版 / Vercel Ready

このフォルダをGitHubリポジトリ直下にそのまま置けば、Vercelで公開できる構成です。

## 重要：404対策済み

- `index(1).html` ではなく、必ず `index.html` として配置済み
- Vercelの公開先を `dist` に固定
- `npm run build` で `dist/index.html` を生成
- `/deck` でも開けるように `rewrites` を設定
- `dist/index.html` も同梱済み

## ファイル構成

```txt
CBA_complete_vercel_ready/
├─ index.html                  # 完成HTML。これ単体でブラウザ表示可能
├─ dist/
│  └─ index.html               # Vercel公開用のコピー
├─ package.json                # Vercelビルド用
├─ vercel.json                 # Vercel設定
├─ slides_data.json            # スライド編集元データ
├─ build_html.py               # slides_data.json → index.html 再生成スクリプト
├─ public/images/
│  ├─ cover_hero.jpg
│  └─ logo.jpg
└─ CBA_deck_original.pdf       # 元PDF
```

## Vercel設定

VercelのProject Settingsで下記にしてください。

```txt
Framework Preset: Other
Install Command: npm install
Build Command: npm run build
Output Directory: dist
Root Directory: GitHubリポジトリ直下
```

再デプロイ時は、必ず **Use existing Build Cache** を外して Redeploy してください。

## 表示URL

```txt
https://xxxx.vercel.app/
https://xxxx.vercel.app/deck
```

どちらでも表示できます。

## 操作

```txt
次へ / 戻る: → ← またはスペース
商談メモ: Nキー
全画面: Fキー
最初 / 最後: Home / End
スマホ: 左右スワイプ、画面右半分/左半分タップ
```

## スライド修正

`slides_data.json` を編集後、ローカルで下記を実行します。

```bash
python build_html.py
npm run build
```

その後、GitHubへpushすればVercelに反映されます。
