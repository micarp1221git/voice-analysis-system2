#!/usr/bin/env python3
import sys
import os
import numpy as np

print("音声分析システム")
print("=" * 50)

# 基本的な分析から始める
audio_files = [
    "AI音声シャドーイング用.wav",
    "安定歌としゃべり.wav", 
    "来週に続く.wav"
]

print("利用可能な音声ファイル:")
available_files = []
for i, file in enumerate(audio_files, 1):
    if os.path.exists(file):
        size_mb = os.path.getsize(file) / (1024*1024)
        print(f"{i}. {file} ({size_mb:.2f} MB)")
        available_files.append(file)

if not available_files:
    print("音声ファイルが見つかりません。")
    sys.exit(1)

# ピッチデータの分析
txt_file = "AI音声シャドーイング用.txt"
if os.path.exists(txt_file):
    print(f"\nピッチデータファイル: {txt_file}")
    
    # ファイルサイズ
    size_kb = os.path.getsize(txt_file) / 1024
    print(f"サイズ: {size_kb:.2f} KB")
    
    # データ読み込み
    try:
        with open(txt_file, 'r') as f:
            lines = f.readlines()
        
        print(f"データ行数: {len(lines)}")
        
        # 最初の5行を表示
        print("\n最初の5行:")
        for i, line in enumerate(lines[:5]):
            parts = line.strip().split('\t')
            if len(parts) == 2:
                time_val, pitch_val = parts
                print(f"  {i+1}: 時間={time_val}秒, ピッチ={pitch_val}Hz")
        
        # 数値データを解析
        times = []
        pitches = []
        for line in lines:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                try:
                    time_val = float(parts[0])
                    pitch_val = float(parts[1])
                    times.append(time_val)
                    pitches.append(pitch_val)
                except ValueError:
                    continue
        
        if times and pitches:
            print(f"\n【ピッチデータ統計】")
            print(f"有効データ点数: {len(pitches)}")
            print(f"時間範囲: {min(times):.3f} - {max(times):.3f} 秒")
            print(f"ピッチ統計:")
            print(f"  平均: {np.mean(pitches):.2f} Hz")
            print(f"  中央値: {np.median(pitches):.2f} Hz")
            print(f"  標準偏差: {np.std(pitches):.2f} Hz")
            print(f"  最小値: {min(pitches):.2f} Hz")
            print(f"  最大値: {max(pitches):.2f} Hz")
            
    except Exception as e:
        print(f"エラー: {e}")

print("\n" + "=" * 50)
print("基本分析完了")
print("=" * 50)

# librosaが利用可能かチェック
print("\n【システムチェック】")
try:
    import librosa
    print("✓ librosa: 利用可能")
    print("  高度な音声分析機能が使えます")
except ImportError:
    print("✗ librosa: 未インストール")
    print("  pip install librosa でインストールしてください")

try:
    import matplotlib.pyplot as plt
    print("✓ matplotlib: 利用可能")
    print("  グラフ作成機能が使えます")
except ImportError:
    print("✗ matplotlib: 未インストール")
    print("  pip install matplotlib でインストールしてください")

try:
    import pandas as pd
    print("✓ pandas: 利用可能")
    print("  データ分析機能が使えます")
except ImportError:
    print("✗ pandas: 未インストール")
    print("  pip install pandas でインストールしてください")