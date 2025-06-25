import streamlit as st
import numpy as np
import librosa
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont
import io
import tempfile
import os
import random
from datetime import datetime

class VoiceAnalyzer:
    def __init__(self):
        self.sample_rate = 22050
        self.metrics_names = {
            'volume': '声の大きさ',
            'clarity': '声の明瞭度',
            'pitch_stability': '音程の安定性',
            'rhythm': 'リズム・テンポ',
            'expression': '表現力',
            'resonance': '声の響き'
        }
        
    def load_audio(self, audio_file):
        """音声ファイルを読み込む"""
        file_extension = audio_file.name.split(".")[-1].lower()
        
        # M4Aファイルの場合は先にエラーメッセージを表示
        if file_extension == 'm4a':
            raise ValueError("M4Aファイルは現在サポートされていません。WAV、MP3ファイルをご利用ください。")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as tmp_file:
            tmp_file.write(audio_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            # より安定した音声読み込み
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                y, sr = librosa.load(tmp_file_path, sr=self.sample_rate, duration=30)
            
            duration = len(y) / sr
            
            # 30秒より長い場合は30秒にトリミング
            if duration > 30:
                y = y[:int(30 * sr)]
                duration = 30.0
            
            os.unlink(tmp_file_path)
            return y, sr, 30.0
            
        except Exception as e:
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
            # より分かりやすいエラーメッセージ
            if "Format not recognised" in str(e):
                raise ValueError(f"音声ファイル形式({file_extension})がサポートされていません。WAVまたはMP3ファイルをご利用ください。")
            raise e
    
    def analyze_voice(self, y, sr, purpose):
        """音声を分析して6つの指標を計算"""
        metrics = {}
        
        # 1. 声の大きさ（RMSエネルギー）
        rms = np.sqrt(np.mean(y**2))
        # 無音部分を除外した計算
        non_silent = y[np.abs(y) > 0.01]
        if len(non_silent) > 0:
            rms_non_silent = np.sqrt(np.mean(non_silent**2))
            volume_score = min(99, int(rms_non_silent * 500))
        else:
            volume_score = 10
        metrics['volume'] = volume_score
        
        # 2. 声の明瞭度（スペクトル重心）
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        clarity_score = min(99, int(np.mean(spectral_centroids) / 40))
        metrics['clarity'] = clarity_score
        
        # 3. 音程の安定性（ピッチの標準偏差）
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)
        
        if len(pitch_values) > 0:
            pitch_std = np.std(pitch_values)
            pitch_stability = max(10, min(99, int(99 - pitch_std / 10)))
        else:
            pitch_stability = 50
        metrics['pitch_stability'] = pitch_stability
        
        # 4. リズム・テンポ（テンポ検出）
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        if purpose == "speaking":
            # 話し声の場合、適度なテンポが良い
            rhythm_score = min(99, int(50 + abs(120 - tempo) / 2))
        else:
            # 歌やプレゼンの場合、安定したテンポが良い
            rhythm_score = min(99, int(tempo / 2))
        metrics['rhythm'] = rhythm_score
        
        # 5. 表現力（変動係数）
        rms_frames = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
        if np.mean(rms_frames) > 0:
            cv = np.std(rms_frames) / np.mean(rms_frames)
            expression_score = min(95, max(30, int(cv * 200)))
        else:
            expression_score = 30
        metrics['expression'] = expression_score
        
        # 6. 声の響き（スペクトルロールオフ）
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        resonance_score = min(99, int(np.mean(rolloff) / 50))
        metrics['resonance'] = resonance_score
        
        # 目的別の重み付け調整
        if purpose == "singing":
            metrics['pitch_stability'] = min(99, int(metrics['pitch_stability'] * 1.2))
            metrics['expression'] = min(95, int(metrics['expression'] * 1.1))
        elif purpose == "speaking":
            metrics['clarity'] = min(99, int(metrics['clarity'] * 1.2))
            metrics['rhythm'] = min(99, int(metrics['rhythm'] * 1.1))
        elif purpose == "presentation":
            metrics['volume'] = min(99, int(metrics['volume'] * 1.1))
            metrics['clarity'] = min(99, int(metrics['clarity'] * 1.1))
        
        return metrics, y, sr
    
    def create_radar_chart(self, metrics, title="音声分析結果"):
        """レーダーチャートを作成"""
        categories = list(self.metrics_names.values())
        values = [metrics[key] for key in self.metrics_names.keys()]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='スコア',
            line_color='rgb(50, 150, 255)',
            fillcolor='rgba(50, 150, 255, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            title=title,
            showlegend=False,
            height=500
        )
        
        return fig
    
    def get_evaluation_level(self, total_score):
        """総合スコアから5段階評価を返す"""
        if total_score >= 450:
            return "S", "プロフェッショナルレベル"
        elif total_score >= 400:
            return "A", "非常に優秀"
        elif total_score >= 350:
            return "B", "良好"
        elif total_score >= 300:
            return "C", "標準的"
        else:
            return "D", "改善の余地あり"
    
    def generate_diagnosis(self, metrics, purpose, name):
        """AI診断テキストを生成"""
        total_score = sum(metrics.values())
        level, level_desc = self.get_evaluation_level(total_score)
        
        # 複数の診断パターンを用意
        patterns = {
            "S": [
                f"{name}の声は素晴らしい完成度です！プロの領域に達しており、すべての指標で高いバランスを保っています。",
                f"驚異的な声質です！{name}の声はプロフェッショナルとして通用する実力を持っています。",
                f"{name}の声の完成度は極めて高いです。全体的なバランスが素晴らしく、プロ級の実力といえるでしょう。"
            ],
            "A": [
                f"{name}の声は非常に優れています。もう少しの練習でプロレベルに到達できる素質を持っています。",
                f"素晴らしい声質です！{name}の声は高い完成度を誇り、さらなる向上の可能性を秘めています。",
                f"{name}の声は非常に良好です。現在の実力を維持しながら、さらに磨きをかけていきましょう。"
            ],
            "B": [
                f"{name}の声は良好な状態です。いくつかの改善点に取り組むことで、さらなる向上が期待できます。",
                f"良い声をお持ちです！{name}の声にはまだ成長の可能性があり、練習次第で大きく向上するでしょう。",
                f"{name}の声は基本的な要素が整っています。特定の分野を重点的に練習することで飛躍的な成長が可能です。"
            ],
            "C": [
                f"{name}の声は標準的なレベルです。基礎からしっかり練習することで、確実に上達していけるでしょう。",
                f"現在の{name}の声は平均的ですが、適切なトレーニングで大きく改善する可能性があります。",
                f"{name}の声には改善の余地があります。焦らず基本から積み上げていくことで、着実に成長できます。"
            ],
            "D": [
                f"{name}の声にはまだ多くの改善点がありますが、それは成長の可能性が大きいということです。基礎練習から始めましょう。",
                f"現在の{name}の声は発展途上です。プロの指導を受けることで、効率的に上達できるでしょう。",
                f"{name}の声は改善の余地が大いにあります。正しい方法で練習すれば、必ず上達します。"
            ]
        }
        
        # ランダムに診断パターンを選択
        diagnosis = random.choice(patterns[level])
        
        # 弱点の分析
        weak_points = []
        for metric, value in metrics.items():
            if value < 60:
                weak_points.append((self.metrics_names[metric], value))
        
        weak_points.sort(key=lambda x: x[1])
        
        if weak_points:
            diagnosis += f"\n\n特に「{weak_points[0][0]}」（{weak_points[0][1]}点）"
            if len(weak_points) > 1:
                diagnosis += f"と「{weak_points[1][0]}」（{weak_points[1][1]}点）"
            diagnosis += "の改善に注力することをお勧めします。"
        
        # 改善のヒント
        hints = []
        if metrics['volume'] < 60:
            hints.append("・呼吸をしっかり使うために、腹式呼吸の練習を行いましょう")
        if metrics['clarity'] < 60:
            hints.append("・滑舌を改善するため、口の開き方と舌の位置を意識しましょう")
        if metrics['pitch_stability'] < 60:
            hints.append("・音程を安定させるため、ロングトーンの練習を取り入れましょう")
        if metrics['rhythm'] < 60:
            hints.append("・リズム感を養うため、メトロノームを使った練習をしましょう")
        if metrics['expression'] < 60:
            hints.append("・表現力を高めるため、感情を込めた朗読練習をしましょう")
        if metrics['resonance'] < 60:
            hints.append("・声の響きを良くするため、共鳴腔を意識した発声練習をしましょう")
        
        if hints:
            diagnosis += "\n\n【改善のヒント】\n" + "\n".join(hints)
        
        return diagnosis, total_score, level, level_desc
    
    def create_result_image(self, name, metrics, diagnosis, total_score, level, radar_fig):
        """結果を画像として出力（JPG形式）"""
        try:
            # 画像サイズ
            width = 1080
            height = 1920
            
            # 背景画像を作成
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            
            # デフォルトフォントを使用
            font = ImageFont.load_default()
            
            # タイトル
            y_pos = 50
            draw.text((width//2, y_pos), "音声分析結果", font=font, fill='black', anchor="mt")
            
            # 名前と日付
            y_pos += 80
            date_str = datetime.now().strftime("%Y年%m月%d日")
            draw.text((width//2, y_pos), f"{name} - {date_str}", font=font, fill='gray', anchor="mt")
            
            # 総合スコア
            y_pos += 80
            draw.text((width//2, y_pos), f"総合スコア: {total_score}/594点", font=font, fill='black', anchor="mt")
            
            # レベル評価
            y_pos += 80
            draw.text((width//2, y_pos), f"評価: {level}", font=font, fill='black', anchor="mt")
            
            # 各指標のスコア
            y_pos += 120
            draw.text((width//2, y_pos), "詳細スコア", font=font, fill='black', anchor="mt")
            y_pos += 60
            
            for key, name_jp in self.metrics_names.items():
                score = metrics[key]
                draw.text((100, y_pos), f"{name_jp}: {score}点", font=font, fill='black')
                y_pos += 40
            
            # AI診断（簡略化）
            y_pos += 40
            draw.text((width//2, y_pos), "AI診断", font=font, fill='black', anchor="mt")
            y_pos += 60
            
            # 診断テキストの最初の部分のみ表示
            first_line = diagnosis.split("。")[0] + "。"
            if len(first_line) > 30:
                first_line = first_line[:27] + "..."
            draw.text((100, y_pos), first_line, font=font, fill='black')
            
            # フッター
            y_pos = height - 100
            draw.text((width//2, y_pos), "© 2024 Voice Analysis AI", font=font, fill='gray', anchor="mt")
            
            # JPG形式で保存
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=95)
            output.seek(0)
            
            return output
        except Exception as e:
            # 画像生成に失敗した場合は例外を再発生
            raise Exception(f"画像生成エラー: {str(e)}")

    def create_share_text(self, name, metrics, diagnosis, total_score, level):
        """X(旧Twitter)シェア用のテキストを生成"""
        # メトリクスをスコア順にソート
        sorted_metrics = sorted(metrics.items(), key=lambda x: x[1], reverse=True)
        
        # 表示順序：最上位、第2位、最下位、第3位
        display_order = [
            sorted_metrics[0],   # 最上位
            sorted_metrics[1],   # 第2位
            sorted_metrics[-1],  # 最下位
            sorted_metrics[2]    # 第3位
        ]
        
        # AI診断から最初の一文を抽出（句点。…の形）
        first_sentence = diagnosis.split("。")[0] + "。"
        if len(first_sentence) > 47:
            first_sentence = first_sentence[:44] + "。"
        first_sentence += "…"
        
        # 星とプログレスバーを作成
        def create_progress_bar(score):
            """スコアに基づいてプログレスバーと星を生成"""
            stars = int(score / 20)  # 20点刻みで星を計算
            star_text = "★" * stars + "☆" * (5 - stars)
            
            # プログレスバー（10ブロック）
            filled = int(score / 10)
            progress = "█" * filled + "░" * (10 - filled)
            
            return f"{star_text} {progress} {score}点"
        
        share_text = f"""🎤音声分析結果
✨{name[:-2]}さんの音声診断結果✨
総合スコア{total_score}点(評価{level})

{first_sentence}

【声の特徴】"""
        
        # メトリクスを上位2つ、最下位、3番目の順に表示
        share_metrics = []
        share_metrics.append(f"{self.metrics_names[display_order[0][0]]}:{display_order[0][1]}点")
        share_metrics.append(f"{self.metrics_names[display_order[1][0]]}:{display_order[1][1]}点")
        share_metrics.append(f"{self.metrics_names[display_order[2][0]]}:{display_order[2][1]}点")
        share_metrics.append(f"{self.metrics_names[display_order[3][0]]}:{display_order[3][1]}点")
        
        share_text += "\n".join(share_metrics)
        share_text += "\n\n#音声分析 #ボイストレーニング #声診断 #AI診断"
        
        return share_text

def main():
    st.set_page_config(
        page_title="AI音声分析", 
        page_icon="🎤", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # 根本的解決：ブラウザのダークモード検出を無効化
    st.markdown("""
    <style>
    /* ブラウザのダークモード検出を完全に無効化 */
    @media (prefers-color-scheme: dark) {
        * {
            color-scheme: light !important;
        }
    }
    
    /* 全要素をライトモードに強制 */
    * {
        color-scheme: light !important;
    }
    
    /* ルート要素の背景を白に固定 */
    html, body, [data-testid="stApp"], .main, .block-container {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Streamlitアプリ全体の設定 */
    .stApp {
        background: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* メインコンテンツエリア */
    .main .block-container {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        padding-top: 2rem !important;
    }
    
    /* ヘッダーとタイトル */
    h1, h2, h3, h4, h5, h6 {
        color: #1E3A8A !important;
        font-weight: 600 !important;
    }
    
    /* テキスト要素 */
    p, span, div, label {
        color: #000000 !important;
    }
    
    /* 入力フィールド - 完全に白背景に */
    .stTextInput > div > div > input {
        background-color: #FFFFFF !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 500 !important;
    }
    .stTextInput > div > div > input:focus {
        background-color: #FFFFFF !important;
        border-color: #2563EB !important;
        color: #000000 !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #64748B !important;
    }
    
    /* セレクトボックス - 超強力な白背景強制 */
    .stSelectbox, 
    .stSelectbox *, 
    .stSelectbox div, 
    .stSelectbox span, 
    .stSelectbox ul, 
    .stSelectbox li {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* セレクトボックス本体 */
    .stSelectbox > div > div {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    
    /* Baseウェブコンポーネント */
    div[data-baseweb="select"],
    div[data-baseweb="select"] *,
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] span,
    [data-baseweb="select"] [role="combobox"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* ドロップダウンメニュー全体 - より強力に */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] *,
    div[data-baseweb="popover"] div,
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li,
    [data-baseweb="popover"],
    [data-baseweb="popover"] * {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    /* ドロップダウンの内部コンテナ */
    [data-baseweb="popover"] > div,
    [data-baseweb="popover"] > div > div {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
    }
    
    /* メニューリスト */
    ul[role="listbox"],
    ul[role="listbox"] *,
    ul[role="listbox"] li {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* 個別の選択肢 */
    li[role="option"],
    li[role="option"] *,
    li[role="option"] div,
    li[role="option"] span {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* ホバー状態 */
    li[role="option"]:hover,
    li[role="option"]:hover *,
    li[role="option"]:hover div,
    li[role="option"]:hover span {
        background-color: #F3F4F6 !important;
        background: #F3F4F6 !important;
        color: #000000 !important;
    }
    
    /* 選択された状態 */
    li[role="option"][aria-selected="true"],
    li[role="option"][aria-selected="true"] * {
        background-color: #E5E7EB !important;
        background: #E5E7EB !important;
        color: #000000 !important;
    }
    
    /* ファイルアップローダー */
    .stFileUploader > div {
        background-color: #F8FAFC !important;
        border: 2px dashed #94A3B8 !important;
        border-radius: 8px !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background-color: #F8FAFC !important;
        color: #000000 !important;
    }
    .stFileUploader label {
        color: #000000 !important;
    }
    
    /* プライマリボタン（分析開始） - 読みやすさ改善 */
    .stButton > button[type="submit"] {
        background-color: #1E3A8A !important;
        border: none !important;
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    .stButton > button[type="submit"]:hover {
        background-color: #1E40AF !important;
        color: #FFFFFF !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* 通常のボタン */
    .stButton > button {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
    }
    .stButton > button:hover {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
    }
    
    /* メトリクスカード */
    [data-testid="metric-container"] {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        color: #000000 !important;
    }
    [data-testid="metric-container"] > div {
        color: #000000 !important;
    }
    [data-testid="metric-container"] label {
        color: #374151 !important;
    }
    
    /* 情報ボックス */
    .stInfo {
        background-color: #EFF6FF !important;
        border-left: 4px solid #3B82F6 !important;
        color: #000000 !important;
    }
    .stInfo > div {
        color: #000000 !important;
    }
    
    /* サクセスメッセージ */
    .stSuccess {
        background-color: #ECFDF5 !important;
        border-left: 4px solid #10B981 !important;
        color: #000000 !important;
    }
    .stSuccess > div {
        color: #000000 !important;
    }
    
    /* エラーメッセージ */
    .stError {
        background-color: #FEF2F2 !important;
        border-left: 4px solid #EF4444 !important;
        color: #000000 !important;
    }
    .stError > div {
        color: #000000 !important;
    }
    
    /* Plotlyチャート背景 */
    .js-plotly-plot {
        background-color: #FFFFFF !important;
    }
    
    /* スピナー */
    .stSpinner > div {
        color: #000000 !important;
    }
    
    /* ダウンロードボタン */
    .stDownloadButton > button {
        background-color: #6B7280 !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    
    /* すべてのテキストを黒に強制 */
    .stMarkdown, .stMarkdown > div, .stText {
        color: #000000 !important;
    }
    
    /* ラジオボタンのスタイリング */
    .stRadio > div {
        background-color: #F8FAFC !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .stRadio label {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    /* 最終手段：すべての要素をライトモードに強制 */
    * {
        filter: none !important;
    }
    
    /* Streamlitのダークモード変数を上書き */
    :root {
        --background-color: #FFFFFF !important;
        --secondary-background-color: #F0F4F8 !important;
        --text-color: #000000 !important;
        color-scheme: light !important;
    }
    
    /* データテーマをライトに強制 */
    [data-theme="dark"] * {
        background-color: inherit !important;
        color: #000000 !important;
    }
    
    /* Base Webのポップオーバーを確実に白背景に */
    [data-baseweb="popover"],
    [data-baseweb="popover"] *,
    [data-baseweb="select"] *,
    [role="listbox"],
    [role="listbox"] *,
    [role="option"],
    [role="option"] * {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        fill: #000000 !important;
    }
    </style>
    
    <script>
        // 根本的解決：MutationObserverで動的要素を監視
        function applyLightTheme(element) {
            if (element && element.style) {
                element.style.setProperty('background-color', '#FFFFFF', 'important');
                element.style.setProperty('background', '#FFFFFF', 'important');
                element.style.setProperty('color', '#000000', 'important');
            }
            
            // 子要素にも適用
            if (element && element.querySelectorAll) {
                const children = element.querySelectorAll('*');
                children.forEach(child => {
                    if (child.style) {
                        child.style.setProperty('background-color', '#FFFFFF', 'important');
                        child.style.setProperty('background', '#FFFFFF', 'important');
                        child.style.setProperty('color', '#000000', 'important');
                    }
                });
            }
        }
        
        // MutationObserverでDOM変更を監視
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        // ポップオーバー要素を検出
                        if (node.getAttribute && node.getAttribute('data-baseweb') === 'popover') {
                            applyLightTheme(node);
                        }
                        
                        // 子要素内のポップオーバーも検出
                        const popovers = node.querySelectorAll('[data-baseweb="popover"]');
                        popovers.forEach(applyLightTheme);
                        
                        // リストボックスも対象
                        const listboxes = node.querySelectorAll('[role="listbox"]');
                        listboxes.forEach(applyLightTheme);
                    }
                });
            });
        });
        
        // DOM全体を監視
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        // 初期実行
        setTimeout(function() {
            document.querySelectorAll('[data-baseweb="popover"], [role="listbox"]').forEach(applyLightTheme);
        }, 100);
    </script>
    """, unsafe_allow_html=True)
    
    st.title("🎤 AI音声分析システム")
    st.markdown("""
    あなたの声をAIが診断します。
    30秒以内の音声ファイルをアップロードしてください。
    """)
    
    # セッション状態の初期化
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'result_image' not in st.session_state:
        st.session_state.result_image = None
    if 'share_text' not in st.session_state:
        st.session_state.share_text = ""
    
    analyzer = VoiceAnalyzer()
    
    # 入力フォーム
    with st.form("analysis_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("お名前", placeholder="必須", help="分析結果に表示されます")
        
        with col2:
            st.markdown("**分析目的を選択**")
            purpose = st.radio(
                "選択してください（必須）",
                ["singing", "speaking", "presentation"],
                format_func=lambda x: {
                    "singing": "歌唱力向上",
                    "speaking": "話し方改善", 
                    "presentation": "プレゼン力向上"
                }.get(x, x),
                index=None
            )
        
        audio_file = st.file_uploader(
            "音声ファイルをアップロード",
            type=['wav', 'mp3'],
            help="WAV、MP3ファイルをご利用ください（30秒以内）"
        )
        
        submitted = st.form_submit_button("分析開始", type="primary", use_container_width=True)
    
    if submitted:
        # バリデーション
        if not name:
            st.error("お名前を入力してください。")
            return
        
        if not purpose:
            st.error("分析目的を選択してください。")
            return
            
        if not audio_file:
            st.error("音声ファイルをアップロードしてください。")
            return
        
        # 名前のフォーマット
        formatted_name = f"{name}さん"
        
        # 分析処理
        with st.spinner('音声を分析中...'):
            try:
                # 音声の読み込み
                y, sr, duration = analyzer.load_audio(audio_file)
                
                # 音声分析
                metrics, y_trimmed, sr = analyzer.analyze_voice(y, sr, purpose)
                
                # AI診断
                diagnosis, total_score, level, level_desc = analyzer.generate_diagnosis(metrics, purpose, formatted_name)
                
                # シェア用テキストの生成（エラーハンドリング付き）
                try:
                    share_text = analyzer.create_share_text(formatted_name, metrics, diagnosis, total_score, level)
                    st.session_state.share_text = share_text
                except Exception as share_error:
                    st.warning(f"シェア用テキスト生成でエラーが発生しました: {str(share_error)}")
                    st.session_state.share_text = ""
                
                # 結果表示
                st.success("分析が完了しました！")
                
                # メトリクス表示
                st.subheader("📊 分析結果")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("総合スコア", f"{total_score}/594点")
                with col2:
                    # 星の表示（レベル別）
                    star_count = {"S": "⭐⭐⭐⭐⭐", "A": "⭐⭐⭐⭐", "B": "⭐⭐⭐", "C": "⭐⭐", "D": "⭐"}.get(level, "⭐")
                    st.metric("評価レベル", f"{level} {star_count}")
                with col3:
                    # パーセンテージ表示
                    percentage = min(99, int(total_score / 594 * 100))
                    st.metric("達成度", f"{percentage}%")
                
                # レーダーチャート
                radar_fig = analyzer.create_radar_chart(metrics, f"{formatted_name}の音声分析結果")
                st.plotly_chart(radar_fig, use_container_width=True)
                
                # 詳細スコア（星とパーセンテージ付き）
                st.subheader("📈 詳細スコア")
                cols = st.columns(3)
                for i, (key, name_jp) in enumerate(analyzer.metrics_names.items()):
                    with cols[i % 3]:
                        score = metrics[key]
                        stars = "⭐" * int(score / 20) + "☆" * (5 - int(score / 20))
                        st.metric(name_jp, f"{score}点 {stars}", f"{score}%")
                
                # AI診断結果
                st.subheader("🤖 AI診断")
                st.info(diagnosis)
                
                # 結果画像の生成（エラーハンドリング付き）
                try:
                    result_image = analyzer.create_result_image(
                        formatted_name, metrics, diagnosis, total_score, level, radar_fig
                    )
                    st.session_state.result_image = result_image
                except Exception as img_error:
                    st.warning(f"画像生成でエラーが発生しましたが、分析は完了しています: {str(img_error)}")
                    st.session_state.result_image = None
                
                st.session_state.analysis_complete = True
                
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
                return
    
    # 画像ダウンロードとシェアボタンを先に配置
    if st.session_state.analysis_complete:
        st.markdown("---")
        st.markdown("### 📸 分析結果をシェア")
        
        if st.session_state.share_text:
            # X(旧Twitter)用のシェアURL作成
            import urllib.parse
            encoded_text = urllib.parse.quote(st.session_state.share_text)
            share_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
            
            st.markdown(f"""
            <a href="{share_url}" target="_blank" style="
                display: inline-block;
                background-color: #1DA1F2;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 6px;
                text-decoration: none;
                font-weight: 600;
            ">📤 Xでシェア</a>
            """, unsafe_allow_html=True)
        
        # ビジネスCTAセクションを最後に配置
        st.markdown("---")
        
        # CTAボタンを大きく目立たせる
        st.markdown("""
        <div style="background-color: #f0f8ff; padding: 30px; border-radius: 10px; text-align: center;">
            <h2 style="color: #1f77b4;">🎯 プロの指導で声を変えませんか？</h2>
            <p style="font-size: 18px; margin: 20px 0; color: #000000;">
                さらに詳しいAI分析を基に、プロのボイストレーナーがあなたに最適なトレーニングプランを提案します。
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("各種サービスを見てみる", type="primary", use_container_width=True):
                st.balloons()
                st.success("予約フォームに移動します...")
                # ここに予約フォームへのリンクや処理を追加

if __name__ == "__main__":
    main()