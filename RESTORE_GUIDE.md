# 🔄 復元ガイド - 壊れた時の戻し方

## 現在の状況
✅ **完全動作版がタグ `v1.0-working` で保存済み**
✅ **改善UI版がタグ `v2.0-improved-ui` で保存済み**
✅ **完全UX版がタグ `v3.0-complete-ux` で保存済み** ← 🆕 NEW!

## 復元方法

### 1. 最新の完全UX版に戻したい場合（推奨）
```bash
git reset --hard v3.0-complete-ux
```

### 2. UI改善版に戻したい場合
```bash
git reset --hard v2.0-improved-ui
```

### 3. 元の動作確認済み版に戻したい場合
```bash
git reset --hard v1.0-working
```

### 4. 特定のファイルだけ戻したい場合
```bash
git checkout v3.0-complete-ux -- ファイル名
```

例：
```bash
git checkout v3.0-complete-ux -- app.py
git checkout v3.0-complete-ux -- streamlit_app.py
```

### 4. 現在の状態を確認
```bash
git status              # 変更されたファイル確認
git diff                # 具体的な変更内容確認
git log --oneline -5    # 最近のコミット確認
git tag                 # 利用可能なタグ確認
```

### 5. 新しい修正をコミットする方法
```bash
git add .
git commit -m "修正内容の説明"
```

### 6. セーフポイントに戻る前の確認
```bash
git stash              # 現在の作業を一時保存
git reset --hard v3.0-complete-ux  # 最新セーフポイントに戻る
git stash pop          # 必要に応じて作業を復元
```

## 🛡️ 安全な作業フロー

1. **修正前**: 現在の状態をコミット
2. **修正中**: こまめにコミット
3. **問題発生**: この復元ガイドを使用
4. **修正完了**: 新しいセーフポイント作成

## セーフポイント履歴

### v3.0-complete-ux (最新) 🆕
- Xシェア文章完全リデザイン済み
- 外部リンク機能実装済み
- 完全なユーザージャーニー実装
- CTAボタン最適化済み

### v2.0-improved-ui
- 文言簡素化済み
- UI/UX改善済み
- ボタンサイズ最適化済み
- XシェアとCTA配置調整済み

### v1.0-working (基本版)
- 全機能動作確認済み
- 依存関係解決済み
- テスト音声ファイル生成済み

## 緊急時のコマンド
```bash
# 最新完全UX版に戻す（推奨）
git reset --hard v3.0-complete-ux

# UI改善版に戻す
git reset --hard v2.0-improved-ui

# 基本動作版に戻す
git reset --hard v1.0-working

# 作業ディレクトリをクリーンアップ
git clean -fd

# 仮想環境も再構築する場合
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**🚨 重要**: `git reset --hard` は現在の変更をすべて失います。心配な場合は事前に `git stash` で保存してください。