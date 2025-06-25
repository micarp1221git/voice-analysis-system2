#!/usr/bin/env python3
"""
テスト用音声ファイル生成スクリプト
様々な特性を持つ合成音声を生成してシステムテストに使用
"""

import numpy as np
import scipy.io.wavfile as wavfile
import os

def generate_sine_wave(frequency, duration, sample_rate=22050, amplitude=0.5):
    """正弦波を生成"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

def generate_noise(duration, sample_rate=22050, amplitude=0.1):
    """ホワイトノイズを生成"""
    samples = int(sample_rate * duration)
    noise = amplitude * np.random.normal(0, 1, samples)
    return noise

def generate_chirp(start_freq, end_freq, duration, sample_rate=22050, amplitude=0.5):
    """周波数が変化する音（チャープ）を生成"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    instantaneous_frequency = start_freq + (end_freq - start_freq) * t / duration
    wave = amplitude * np.sin(2 * np.pi * np.cumsum(instantaneous_frequency) / sample_rate)
    return wave

def generate_test_files():
    """テスト用音声ファイルを生成"""
    sample_rate = 22050
    duration = 3.0  # 3秒
    
    # テストディレクトリを作成
    os.makedirs("test_audio", exist_ok=True)
    
    # 1. 純音（440Hz - A4）
    pure_tone = generate_sine_wave(440, duration, sample_rate)
    wavfile.write("test_audio/pure_tone_440hz.wav", sample_rate, 
                 (pure_tone * 32767).astype(np.int16))
    
    # 2. 低い音（220Hz - A3）
    low_tone = generate_sine_wave(220, duration, sample_rate)
    wavfile.write("test_audio/low_tone_220hz.wav", sample_rate, 
                 (low_tone * 32767).astype(np.int16))
    
    # 3. 高い音（880Hz - A5）
    high_tone = generate_sine_wave(880, duration, sample_rate)
    wavfile.write("test_audio/high_tone_880hz.wav", sample_rate, 
                 (high_tone * 32767).astype(np.int16))
    
    # 4. チャープ（周波数変化）
    chirp = generate_chirp(200, 800, duration, sample_rate)
    wavfile.write("test_audio/chirp_200_800hz.wav", sample_rate, 
                 (chirp * 32767).astype(np.int16))
    
    # 5. 複合音（和音）
    chord = (generate_sine_wave(261.63, duration, sample_rate, 0.3) +  # C4
             generate_sine_wave(329.63, duration, sample_rate, 0.3) +  # E4
             generate_sine_wave(392.00, duration, sample_rate, 0.3))   # G4
    wavfile.write("test_audio/chord_c_major.wav", sample_rate, 
                 (chord * 32767).astype(np.int16))
    
    # 6. ノイズ付きトーン
    noisy_tone = generate_sine_wave(440, duration, sample_rate, 0.7) + \
                 generate_noise(duration, sample_rate, 0.1)
    wavfile.write("test_audio/noisy_tone.wav", sample_rate, 
                 (noisy_tone * 32767).astype(np.int16))
    
    # 7. 静寂（非常に小さな音）
    silence = generate_noise(duration, sample_rate, 0.001)
    wavfile.write("test_audio/near_silence.wav", sample_rate, 
                 (silence * 32767).astype(np.int16))
    
    print("テスト用音声ファイルを生成しました:")
    print("- test_audio/pure_tone_440hz.wav (純音 440Hz)")
    print("- test_audio/low_tone_220hz.wav (低音 220Hz)")
    print("- test_audio/high_tone_880hz.wav (高音 880Hz)")
    print("- test_audio/chirp_200_800hz.wav (周波数変化)")
    print("- test_audio/chord_c_major.wav (Cメジャーコード)")
    print("- test_audio/noisy_tone.wav (ノイズ付きトーン)")
    print("- test_audio/near_silence.wav (静寂)")

if __name__ == "__main__":
    generate_test_files()