#!/bin/bash

echo "🚀 音声分析システム デプロイスクリプト"
echo "======================================"
echo ""
echo "GitHubユーザー名を入力してください:"
read github_username

echo ""
echo "リポジトリ名を入力してください (デフォルト: voice-analysis-system):"
read repo_name
repo_name=${repo_name:-voice-analysis-system}

echo ""
echo "以下の設定でGitHubにプッシュします:"
echo "ユーザー: $github_username"
echo "リポジトリ: $repo_name"
echo ""
echo "続行しますか? (y/n)"
read confirm

if [ "$confirm" = "y" ]; then
    echo "GitHubにプッシュ中..."
    git remote add origin https://github.com/$github_username/$repo_name.git
    git branch -M main
    git push -u origin main
    git push origin --tags
    
    echo ""
    echo "✅ 完了!"
    echo ""
    echo "次のステップ:"
    echo "1. https://streamlit.io/cloud にアクセス"
    echo "2. GitHubでログイン"
    echo "3. 'New app'をクリック"
    echo "4. Repository: $github_username/$repo_name"
    echo "5. Branch: main"
    echo "6. Main file: app.py"
    echo "7. 'Deploy!'をクリック"
    echo ""
    echo "デプロイURL: https://$repo_name.streamlit.app (予定)"
else
    echo "キャンセルしました"
fi