# 🚀 音声診断システム デプロイガイド

## 📋 概要
音声診断システムをStreamlit Cloudで無料デプロイする手順書です。

## 🎯 完成したMVP機能
- ✅ 音声アップロード（30秒制限）
- ✅ リアルタイム音声分析（6指標）
- ✅ インタラクティブ可視化
- ✅ AI診断文生成
- ✅ Whisper音声認識（オプション）
- ✅ レスポンシブデザイン
- ✅ ビジネスCTA機能

## 🛠️ ローカル実行手順

### 1. 依存関係インストール
```bash
# 基本版（音声認識なし）
pip install streamlit librosa plotly soundfile pandas matplotlib numpy

# 完全版（音声認識あり）
pip install streamlit librosa plotly soundfile pandas matplotlib numpy openai-whisper
```

### 2. アプリケーション起動
```bash
streamlit run streamlit_app.py
```

### 3. ブラウザアクセス
```
http://localhost:8501
```

## ☁️ Streamlit Cloud デプロイ手順

### 前準備
1. **GitHubアカウント**が必要
2. **Streamlit Cloud**アカウント作成（無料）
3. **リポジトリ作成**

### Step 1: GitHubリポジトリ作成
```bash
# 新しいリポジトリを作成
git init
git add .
git commit -m "Initial commit: Voice Analysis MVP"

# GitHubにプッシュ
git remote add origin https://github.com/your-username/voice-analysis-mvp.git
git push -u origin main
```

### Step 2: requirements.txt調整
デプロイ用の軽量版を作成：
```txt
streamlit>=1.28.0
librosa>=0.10.0
numpy>=1.21.0
matplotlib>=3.5.0
pandas>=1.3.0
plotly>=5.0.0
soundfile>=0.12.0
scipy>=1.7.0
```

### Step 3: Streamlit Cloudデプロイ
1. [share.streamlit.io](https://share.streamlit.io) にアクセス
2. GitHubでログイン
3. 「New app」をクリック
4. リポジトリ選択: `your-username/voice-analysis-mvp`
5. Main file path: `streamlit_app.py`
6. 「Deploy!」をクリック

### Step 4: デプロイ完了
- 自動でビルド開始
- 数分後にURLが発行される
- 例: `https://your-app-name.streamlit.app`

## 🔧 設定ファイル

### .streamlit/config.toml（オプション）
```toml
[server]
maxUploadSize = 16

[theme]
primaryColor = "#2E86AB"
backgroundColor = "#F8F9FA"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#262730"
```

## 📊 システム要件

### Streamlit Cloud制限
- **メモリ**: 800MB
- **CPU**: 1コア
- **ストレージ**: 一時的
- **ファイルサイズ**: 最大200MB

### 推奨設定
- **音声ファイル**: 30秒以下
- **Whisper**: tinyモデル使用（軽量）
- **可視化**: 適度な解像度

## 🐛 トラブルシューティング

### よくある問題

#### 1. メモリ不足
```python
# 軽量化オプション
matplotlib.use('Agg')
whisper.load_model("tiny")  # baseではなくtiny
```

#### 2. デプロイエラー
```bash
# requirements.txtの依存関係確認
pip freeze > requirements_check.txt
```

#### 3. 音声処理エラー
```python
# エラーハンドリング強化済み
try:
    y, sr = librosa.load(file_path)
except Exception as e:
    st.error(f"音声読み込みエラー: {e}")
```

## 💰 コスト構造

### 無料プラン
- **Streamlit Cloud**: 完全無料
- **基本機能**: すべて無料
- **制限**: 合理的な範囲内

### 有料拡張（オプション）
- **OpenAI API**: 月$5-20程度
- **カスタムドメイン**: $20/月
- **プレミアム機能**: 必要に応じて

## 🎯 ビジネス活用

### 即座に可能
1. **無料診断**でリード獲得
2. **¥9,800コンサル**への誘導
3. **データ収集**で改善

### 成長戦略
1. **ユーザーフィードバック**収集
2. **機能拡張**（GPT API追加等）
3. **収益化**テスト

## 📈 次のステップ

### 短期（1-2週間）
- [ ] 実際のユーザーテスト
- [ ] フィードバック収集
- [ ] 細かな改善

### 中期（1ヶ月）
- [ ] GPT API統合
- [ ] PDF生成機能
- [ ] ユーザー管理

### 長期（3ヶ月）
- [ ] 収益化実装
- [ ] スケーリング
- [ ] 追加サービス

## 📞 サポート

問題が発生した場合：
1. **Streamlit Cloud logs**を確認
2. **GitHub Issues**で質問
3. **Streamlit Community**フォーラム活用

---

🎉 **MVPの完成おめでとうございます！**
音声診断ビジネスの第一歩を踏み出せます。