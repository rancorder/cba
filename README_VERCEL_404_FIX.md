# Vercel 404対策 完全修正版

このパッケージは、Vercelで404にならないように **dist公開方式** に固定しています。

## 公開されるURL

- `/` : スライドのみ（index.html）
- `/deck` : スライドのみ（index.html）
- `/present` : 商談者用ビュー（present.html）
- `/present.html` : 商談者用ビュー（present.html）

## Vercel設定

Project Settings → Build and Development Settings

- Framework Preset: Other
- Install Command: npm install
- Build Command: npm run build
- Output Directory: dist
- Root Directory: リポジトリ直下

## 重要

Redeployするときは必ず **Use existing Build Cache** を外してください。

## 何をしているか

`npm run build` で以下を作ります。

```txt
dist/
├─ index.html
├─ deck/
│  └─ index.html
├─ present.html
└─ present/
   └─ index.html
```

これにより、Vercelが `/`, `/deck`, `/present`, `/present.html` のどれを見ても表示できます。
