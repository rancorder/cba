# CBA 商談プレゼン（ターゲット②：音楽経験者・再起層）

データ駆動の横スライドプレゼン。1ファイル完結（`index.html`）。

## すぐ使う

`index.html` をブラウザで開くだけ。

| 操作 | キー |
|---|---|
| 次へ / 戻る | → ← （またはスペース） |
| 商談メモ（商談者専用） | **N** キー or 画面下「商談メモ」ボタン |
| 全画面 | **F** キー or「全画面」ボタン |
| 最初 / 最後 | Home / End |
| スマホ | 左右スワイプ・画面の右半分/左半分タップ |

- **/deck（聴衆が見る画面）**＝通常表示
- **商談メモ（N キー）**＝商談者専用カンペ。聴衆には表示されない。各スライドの「話す内容」と「進行のポイント」を表示

## Vercelにデプロイ（3人で共有用URL）

### 方法A：ドラッグ&ドロップ（最速・GitHub不要）
1. https://vercel.com にログイン
2. このフォルダ（`cba-deck`）ごと Vercel の「New Project」にドラッグ
3. デプロイ完了→ `https://〇〇.vercel.app` が発行される
4. URLを商談者3人に共有

### 方法B：GitHub連携（修正を継続する場合）
1. このフォルダをGitHubリポジトリにpush
2. VercelでImport→自動デプロイ
3. 以後 `slides_data.json` を編集してpushするだけで全員に反映

## スライドを追加・修正する

**`slides_data.json` の `slides` 配列を編集 → `python3 build_html.py` を実行**するだけ。

```jsonc
{
  "id": "新スライドID",
  "type": "statement",        // 下の型一覧から選ぶ
  "section": "証拠",           // 画面左上に出る章ラベル
  "badge": "営業独自",         // 任意。商談メモにバッジ表示
  "deck": { ... },            // 聴衆が見る内容（型ごとに項目が違う）
  "notes": {                  // 商談者カンペ（聴衆に出ない）
    "talk": "実際に話す台本",
    "cue": "進行のポイント・注意"
  }
}
```

配列の好きな位置に差し込めば、その順序で表示される。

### 使える型（type）
| type | 用途 | deckの主な項目 |
|---|---|---|
| `cover` | 表紙 | lead, title, sub, en, hero, logo |
| `statement` | 一文を大きく見せる | eyebrow, title（`<em>`で帯マーカー） |
| `agenda` | 番号付き3項目＋締め | title, items[], foot |
| `curator` | ★紹介者の理由 | eyebrow, title, reasons[], sign |
| `reflect` | 問いかけ（答えは口頭） | eyebrow, title, lines[], foot |
| `testimonial` | 受講生の声 | title, meta, headline, quote[] |
| `service` | サービス内容リスト | title, items[[見出し,説明]], foot |
| `cards` | 横並びカード | title, cards[], foot |
| `diagnostic` | ★3つの自己診断 | eyebrow, title, lead, questions[], close |
| `price` | 料金プラン | title, plans[[名,額,説明]], note, foot |
| `special` | 特典二択 | title, lead, options[[ラベル,本文,補足]] |
| `contract` | 契約条件（返金は自動で強調） | title, points[[項目,内容]] |
| `closing` | 次のステップ | eyebrow, title, steps[], foot |

## 重要な運用ルール（厳守）

- **価格スライドに「音大4年 vs 半年」の同等比較を書かない。** 口頭のみ（商談メモに明記済み）。誇大表示リスク回避のため
- **元の145枚PDFに無い数値・実績は追加しない。** すべて原本由来の事実のみ
- **返金不可（契約スライド）は口頭でも必ず明示し、相手の同意を取ってから次へ進む**
- **受講生の顔写真は使っていない。** 使う場合はCBAから個別許諾を取ること
- curatorスライドの `sign` の `［ 氏名・肩書 ］` を、商談者ごとに自分の名前に書き換える

## ファイル構成
```
cba-deck/
├─ index.html          ← 完成品（これ単体で動く）
├─ slides_data.json    ← スライドの中身（ここを編集）
├─ build_html.py       ← json→html 再生成スクリプト
├─ vercel.json         ← Vercel設定
└─ public/images/      ← 画像（base64でindex.htmlに埋め込み済み）
```
