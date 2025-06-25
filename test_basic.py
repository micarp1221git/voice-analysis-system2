#!/usr/bin/env python3
"""
基本機能テスト - 依存関係なしでコア機能をテスト
"""
import librosa
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

def test_voice_analysis():
    """既存の音声ファイルで基本分析をテスト"""
    print("🎤 音声分析システム - 基本テスト")
    print("=" * 50)
    
    # 利用可能な音声ファイルをチェック
    audio_files = [
        "test_audio/pure_tone_440hz.wav",
        "test_audio/chord_c_major.wav",
        "test_audio/noisy_tone.wav",
        "AI音声シャドーイング用.wav",
        "安定歌としゃべり.wav", 
        "来週に続く.wav"
    ]
    
    test_file = None
    for file in audio_files:
        if os.path.exists(file):
            test_file = file
            break
    
    if not test_file:
        print("❌ テスト用音声ファイルが見つかりません")
        return False
    
    print(f"📁 テストファイル: {test_file}")
    
    try:
        # 音声読み込み
        print("🔄 音声ファイル読み込み中...")
        y, sr = librosa.load(test_file)
        duration = len(y) / sr
        print(f"✅ 読み込み成功: {duration:.2f}秒, {sr}Hz")
        
        # 基本分析
        print("🔍 特徴量抽出中...")
        
        # RMS (音量)
        rms = librosa.feature.rms(y=y)[0]
        avg_volume = float(np.mean(rms))
        volume_stability = float(np.std(rms))
        
        # ピッチ分析
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)
        
        # 結果表示
        print("\n📊 分析結果:")
        print(f"   音声長: {duration:.2f}秒")
        print(f"   平均音量: {avg_volume:.6f}")
        print(f"   音量安定性: {volume_stability:.6f}")
        
        if pitch_values:
            pitch_mean = float(np.mean(pitch_values))
            pitch_std = float(np.std(pitch_values))
            print(f"   平均ピッチ: {pitch_mean:.2f}Hz")
            print(f"   ピッチ範囲: {np.min(pitch_values):.2f} - {np.max(pitch_values):.2f}Hz")
            print(f"   ピッチ安定性: {1.0 / (1.0 + pitch_std / pitch_mean):.3f}")
        
        # スペクトラル特徴
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        
        print(f"   音の明るさ: {np.mean(spectral_centroids):.2f}Hz")
        print(f"   明瞭度指標: {np.mean(zcr):.6f}")
        
        # 30秒制限テスト
        print(f"\n⏱️  30秒制限チェック:")
        if duration <= 30:
            print(f"   ✅ OK ({duration:.2f}秒 ≤ 30秒)")
        else:
            print(f"   ❌ 制限超過 ({duration:.2f}秒 > 30秒)")
        
        print("\n🎯 診断例:")
        if avg_volume > 0.03:
            print("   ✅ 適切な音量で話せています")
        else:
            print("   ⚠️  もう少し大きな声で話すとよいでしょう")
        
        if pitch_values and len(pitch_values) > 10:
            pitch_stability = 1.0 / (1.0 + pitch_std / pitch_mean)
            if pitch_stability > 0.7:
                print("   ✅ ピッチが安定しており、聞き取りやすい声です")
            else:
                print("   ⚠️  ピッチの安定性を向上させると印象が良くなります")
        
        print("\n🚀 基本分析テスト完了!")
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def test_dependencies():
    """依存関係のテスト"""
    print("\n🔧 依存関係チェック:")
    
    dependencies = [
        ('librosa', 'librosa'),
        ('numpy', 'numpy'), 
        ('matplotlib', 'matplotlib.pyplot'),
        ('pandas', 'pandas')
    ]
    
    available = []
    missing = []
    
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"   ✅ {name}: 利用可能")
            available.append(name)
        except ImportError:
            print(f"   ❌ {name}: 未インストール")
            missing.append(name)
    
    print(f"\n📋 利用可能: {len(available)}/{len(dependencies)}")
    
    if missing:
        print(f"📦 インストール必要: {', '.join(missing)}")
        print("\n💡 インストールコマンド:")
        print("pip install streamlit librosa plotly soundfile pandas")
    
    return len(missing) == 0

if __name__ == "__main__":
    print("🎤 音声診断システム - 基本機能テスト")
    print("=" * 60)
    
    # 依存関係チェック
    deps_ok = test_dependencies()
    
    # 音声分析テスト
    analysis_ok = test_voice_analysis()
    
    print("\n" + "=" * 60)
    if deps_ok and analysis_ok:
        print("🎉 すべてのテストが成功しました!")
        print("💡 次のステップ: streamlit run streamlit_app.py")
    else:
        print("⚠️  一部の機能で問題があります")
        if not deps_ok:
            print("   - 依存関係をインストールしてください")
        if not analysis_ok:
            print("   - 音声ファイルや分析処理を確認してください")
    print("=" * 60)