# CBA「サウンドヒーリング アーティスト・インストラクター育成講座」商談プレゼン

クリスタルシンギングボウル・ビューティー・アカデミー（CBA）の個別相談（アカデミー説明会）で使う、データ駆動の横スライドプレゼン。台本とスライドが連動する。

- **全70スライド**（共通43枚＋ターゲット別 各9枚 × 3）
- **3ターゲット対応**：A=主婦・会社員／B=音楽経験者・再起層／C=ヨガ・フィットネス講師
  URL末尾に `?target=A` / `?target=B` / `?target=C` を付けると、そのターゲット向けの差し替えスライドが表示される（無指定はB）
- 世界観：**繭 → 脱皮 → 羽化**（スライド＝変容の言葉／台本＝心理段階の手引き）

---

## 2つの使い方

### ★ present.html（個別相談担当者用・推奨）
**台本とスライドが連動する商談ビュー。** これを開けば商談が回る。

- **左**：商談台本（各スライドの「話す内容」「進行のポイント」）。上から読み進める
- **右**：顧客に見せるスライドのプレビュー
- **左の台本ブロックをクリック** → 右のプレビューが切り替わる
- **「🖥 顧客画面を別タブで開く」ボタン** → 別タブに顧客用スライド（操作ボタン無しのクリーン表示）が開く。以降、商談者タブで台本をクリック／← →キーを押すと、別タブのスライドが自動で連動する
- 別タブが繋がると、ボタン横の表示が「顧客画面：接続中」（緑）になる

**Zoom商談の流れ：**
1. `present.html` を開く
2. 「🖥 顧客画面を別タブで開く」を押す → 別タブが開く（＝顧客用スライド）
3. その**別タブだけ**をZoomで画面共有（必要なら別タブで全画面化）
4. 商談者は手元の `present.html` で台本を見ながらクリックで進める → 共有中のスライドが追従

※ 同期は **同じPC・同じブラウザ**で2タブを開く前提（BroadcastChannel）。別端末では同期しません。

### index.html（スライドのみ）
スライドだけの通常表示。台本なし。録画配布やシンプルに見せたい時用。
→ ← で送り、N キーで商談メモ、F キーで全画面。

---

## 公開URL（Vercel）

| URL | 中身 |
|---|---|
| `https://cba-iota.vercel.app/` | スライドのみ（index.html） |
| `https://cba-iota.vercel.app/present` | 個別相談担当者用ビュー（present.html） |
| `https://cba-iota.vercel.app/present.html` | 同上 |

ターゲット切替例：`https://cba-iota.vercel.app/?target=A`

### デプロイの仕組み（重要・現状）

- **`main` ブランチにpushすると Vercel が自動で再デプロイ**する。
- ルーティングは **`vercel.json` の rewrites** で制御（`/` → `/index.html`、`/present` → `/present.html`）。
- **配信はリポジトリ直下（root）方式。** `index.html` / `present.html` をrootに置けば表示される。
- `npm run build` は**使っていない**（`package.json` は無い）。HTMLは下記のPythonスクリプトで手動生成する。

#### `dist/` について
`dist/` は過去のVercel 404対策の名残で、root と同じ内容を複製した保険のフォルダ。**現在は root と dist を同一内容に揃えてある**ので、Vercelがどちらを配信しても同じ結果になる。

- **編集したら root と dist の両方を更新する**（食い違うと、配信元によって古い表示が出る事故になる）。
- `dist/` を削除したい場合は、**先に Vercel の Settings → Build & Deployment → Output Directory が空欄（＝root配信）になっていることを確認**してから消すこと。`dist` 指定のまま消すと404になる。

#### 再デプロイ時の注意
Vercelで Redeploy するときは **「Use existing Build Cache」のチェックを外す**（キャッシュで古い表示が残るのを防ぐ）。

---

## スライドを追加・修正する

1. **`slides_data.json` の `slides` 配列を編集**（台本は各スライドの `notes`：talk / cue）
2. `python3 build_html.py && python3 build_present.py` を実行 → index.html / present.html が再生成される
3. **生成された index.html / present.html を `dist/` 側にも反映**（`dist/index.html`・`dist/deck/index.html`＝index.html、`dist/present.html`・`dist/present/index.html`＝present.html）
4. `main` にpush

```jsonc
{
  "id": "新スライドID",
  "type": "statement",        // 下の型一覧から選ぶ
  "section": "ヒアリング",      // 画面左上に出る章ラベル
  "target": "all",            // all / A / B / C
  "deck": { ... },            // 顧客が見る内容（型ごとに項目が違う）
  "notes": {                  // 商談者カンペ（顧客に出ない）
    "talk": "実際に話す台本",
    "cue":  "進行のポイント・注意"
  }
}
```

### セクション構成（章の順番）
導入 → 権威性 → ヒアリング → 未来 → 半年の歩み → 羽化した人たち → 意思決定 → この道への一歩 → FAQ → 新しい始まり

### 使える型（type）
`cover`（表紙）, `statement`（一文を大きく）, `agenda`（番号付き項目）, `curator`（紹介者の自己紹介）, `reflect`（問いかけ）, `diagnostic`（自己診断）, `service`（内容リスト）, `cards`（横並びカード）, `split`（写真＋テキスト）, `photo`／`photogrid`／`photostat`（写真主体）, `testimonial`（受講生の声）, `concern`（不安への回答）, `plantable`／`plancompare`（プラン比較）, `price`（料金）, `special`（特典）, `contract`（契約条件）, `closing`（次のステップ）

---

## 運用ルール（厳守）

- **正式名称は「サウンドヒーリング アーティスト・インストラクター育成講座」。** 初出は必ずフルで。「アーティスト」「インストラクター」は別コースではなく、これでひとつの講座名。
- **生徒の収益例（金額の表）は載せない。** 収益事例スライドは削除済み。「月◯万円」等の生徒の収入を示す数値は出さない（成約を妨げるため）。残してよい金額は、講座価格・特典相当額・継続コース価格（聞かれた場合のみ）のみ。
- **収益の保証はしない。** 保証スライドは演奏・技術の習得に関するもののみ。
- **未来像で具体的な金額・単価を前面に出さない**（特にfuture-stage／market系）。「自由に表現して生きる」「選ばれる喜び」など、人生・あり方の側で語る。
- **返金不可（契約スライド）は口頭でも必ず明示し、相手の同意を取ってから次へ進む。**
- **受講生の顔写真の使用は、CBAから個別許諾を取ってから。**
- curator（自己紹介）スライドは、商談者ごとに自分の自己紹介に書き換える（経歴自慢ではなく、自己開示・共体験・「一緒に」の構成）。

---

## ファイル構成
```
（リポジトリ直下）
├─ index.html          ← スライドのみ表示版（root配信の本体）
├─ present.html        ← ★個別相談担当者用（台本＋スライド連動）
├─ slides_data.json    ← スライド＋台本の中身（ここを編集して再生成）
├─ build_html.py       ← slides_data.json → index.html 再生成
├─ build_present.py    ← slides_data.json → present.html 再生成
├─ vercel.json         ← Vercel設定（rewrites：root配信）
├─ public/images/      ← 元画像（index.htmlにはbase64で埋め込み済み）
└─ dist/               ← root と同一内容の複製（保険）
   ├─ index.html
   ├─ deck/index.html
   ├─ present.html
   └─ present/index.html
```

---

## 変更履歴（要点）
- 講座名を正式名称「サウンドヒーリング アーティスト・インストラクター育成講座」に統一（表紙タイトル・ブラウザタイトル）。長い名称に合わせ表紙CSSを調整。
- 生徒の収益事例（金額表）スライドを削除。未来像の金額・単価表現を定性表現に軟化。
- root と dist の内容を全70スライドで統一（配信元の食い違いによる古い表示を解消）。
