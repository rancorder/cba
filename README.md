# CBA 商談プレゼン（ターゲット②：音楽経験者・再起層）

データ駆動の横スライドプレゼン。**40枚**、商談台本連動。


## 【重要】Vercel 404対策済み

この版は `dist` 公開方式に修正済みです。

- `/` → スライドのみ
- `/deck` → スライドのみ
- `/present` → 商談者用ビュー
- `/present.html` → 商談者用ビュー

Vercel側は以下にしてください。

```txt
Framework Preset: Other
Install Command: npm install
Build Command: npm run build
Output Directory: dist
Root Directory: リポジトリ直下
```

再デプロイ時は **Use existing Build Cache を外す** こと。


## 2つの使い方

### ★ present.html（商談者用・推奨）
**台本とスライドが1画面で連動する商談ビュー。** これを開けば商談が回る。

- **左**：商談台本（40枚分の「話す内容」「進行のポイント」）。上から読み進める
- **右**：顧客に見せるスライド本体
- **左の台本ブロックをクリック** → 右のスライドが連動して切り替わる
- **「⛶ 顧客に全画面表示」ボタン** → 右のスライドだけが全画面に。Zoomでこの画面を共有すれば、**顧客には台本が一切見えない**
- 全画面中は ← → キーまたは画面クリックでスライド送り。Escで商談者ビューに戻る

**Zoom商談の流れ：**
1. `present.html` を開く
2. 「顧客に全画面表示」を押す → 全画面のスライドウィンドウになる
3. それをZoomで画面共有
4. （別モニタ or 手元で）台本を見ながら、クリックで進める

### index.html（聴衆画面のみ）
スライドだけの通常表示。台本なし。録画配布やシンプルに見せたい時用。
- → ← 送り、N キーで商談メモ、F キーで全画面

## Vercelデプロイ済みなら
- 商談者用： `https://〇〇.vercel.app/present.html`
- スライドのみ： `https://〇〇.vercel.app/`（= index.html）

両ファイルともリポジトリ直下に置けば、URL末尾を変えるだけで切り替わる。

---

## スライドを追加・修正する

**`slides_data.json` の `slides` 配列を編集 → `python3 build_html.py && python3 build_present.py` を実行**するだけ。両ファイル（index.html / present.html）が同じ内容で再生成される。台本は各スライドの `notes`（talk / cue）を編集。

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
├─ present.html        ← ★商談者用（台本＋スライド連動）これを使う
├─ index.html          ← スライドのみ表示版
├─ slides_data.json    ← スライド＋台本の中身（ここを編集）
├─ build_html.py       ← json→index.html 再生成
├─ build_present.py    ← json→present.html 再生成
├─ vercel.json         ← Vercel設定
└─ public/images/      ← 画像（base64でhtmlに埋め込み済み）
```
