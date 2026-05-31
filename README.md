# CBA 商談プレゼン（ターゲット②：音楽経験者・再起層）

データ駆動の横スライドプレゼン。**40枚**、商談台本連動。

## 2つの使い方

### ★ present.html（商談者用・推奨）
**台本とスライドが連動する商談ビュー。** これを開けば商談が回る。

- **左**：商談台本（40枚分の「話す内容」「進行のポイント」）。上から読み進める
- **右**：顧客に見せるスライドのプレビュー
- **左の台本ブロックをクリック** → 右のプレビューが切り替わる
- **「🖥 顧客画面を別タブで開く」ボタン** → 別タブに顧客用スライド（操作ボタン無しのクリーン表示）が開く。以降、**商談者タブで台本をクリック／← →キーを押すと、別タブのスライドが自動で連動**する
- 別タブが繋がると、ボタン横の表示が「顧客画面：接続中」（緑）になる

**Zoom商談の流れ：**
1. `present.html` を開く
2. 「🖥 顧客画面を別タブで開く」を押す → 別タブが開く（＝顧客用スライド）
3. その**別タブだけ**をZoomで画面共有（必要なら別タブで F11 などで全画面化）
4. 商談者は手元の `present.html` で台本を見ながらクリックで進める → 共有中のスライドが追従

※ 同期は **同じPC・同じブラウザ**で2タブを開く前提（BroadcastChannel）。別端末では同期しません。

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
