# CBA Deck - Vercel fixed package

## 重要
Vercelで404になる典型原因は、完成HTMLが `index.html` ではなく `index(1).html` など別名になっていること、または `/deck` にアクセスしているのに `vercel.json` のrewriteが無いことです。

このパッケージでは以下を修正済みです。

- `index(1).html` を `index.html` にリネーム
- `/deck` で開いても `index.html` を表示する `vercel.json` を追加
- 画像は `index.html` にbase64埋め込み済みなので、基本は `index.html` 単体で表示可能

## GitHub → Vercel 手順

1. このフォルダの中身をGitHubリポジトリ直下に置く
2. GitHubへpush
3. VercelでImport
4. Framework Preset は Other / Static を選ぶ
5. Build Command は空欄
6. Output Directory は空欄（または `.`）
7. Deploy

## URL

- `/` で表示
- `/deck` でも表示

## 編集する場合

`slides_data.json` を編集したあと、ローカルで以下を実行してください。

```bash
python build_html.py
```

生成された `index.html` をcommit / pushしてください。
