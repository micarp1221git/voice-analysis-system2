import streamlit as st
import librosa
import numpy as np
import time

# ページ設定
st.set_page_config(
    page_title="音声診断システムデモ",
    page_icon="🎤",
    layout="wide"
)

# カスタムCSS
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
    color: #2E86AB;
    text-align: center;
}
.result-box {
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #2E86AB;
}
</style>
""", unsafe_allow_html=True)

# タイトル
st.markdown('<p class="big-font">🎤 音声診断システム</p>', unsafe_allow_html=True)
st.markdown('<center>あなたの声を分析して、改善のヒントをお届けします</center>', unsafe_allow_html=True)
st.markdown("---")

# サイドバー
with st.sidebar:
    st.header("📊 システム情報")
    st.info("最大30秒の音声ファイルを分析します")
    
    st.markdown("### 🛠️ 利用可能機能")
    st.success("✅ 音声分析")
    st.success("✅ 可視化")
    st.success("✅ AI診断")
    
    st.markdown("### 📈 分析指標")
    st.markdown("""
    - 音量
    - ピッチ安定性
    - 明瞭度
    - 音の豊かさ
    - 音の明るさ
    """)

# メインコンテンツ
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 入力フォーム")
    
    # 入力フォーム
    name = st.text_input("お名前（ニックネーム可）", value="田中太郎")
    purpose = st.selectbox(
        "分析の目的",
        ["話し声の印象", "歌", "プレゼン対策", "その他"]
    )
    
    uploaded_file = st.file_uploader(
        "音声ファイルをアップロード（最大30秒）",
        type=['wav', 'mp3', 'm4a', 'flac'],
        help="WAV, MP3, M4A, FLAC形式に対応"
    )

with col2:
    st.header("🎯 クイックガイド")
    st.markdown("""
    1. **名前を入力**
    2. **目的を選択**
    3. **音声をアップロード**
    4. **分析開始をクリック**
    
    30秒で結果が表示されます！
    """)

# 分析ボタン
if st.button("🔍 分析開始", type="primary", use_container_width=True):
    if uploaded_file is None:
        st.error("音声ファイルをアップロードしてください")
    else:
        # プログレスバー表示
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 分析シミュレーション
        for i in range(100):
            progress_bar.progress(i + 1)
            if i < 20:
                status_text.text(f'音声ファイルを検証中... {i+1}%')
            elif i < 50:
                status_text.text(f'音声を分析中... {i+1}%')
            elif i < 80:
                status_text.text(f'グラフを作成中... {i+1}%')
            else:
                status_text.text(f'診断文を生成中... {i+1}%')
            time.sleep(0.02)
        
        status_text.text('分析完了！')
        
        # 結果表示
        st.balloons()
        st.success("✅ 分析が完了しました！")
        
        # タブで結果表示
        tab1, tab2, tab3, tab4 = st.tabs(["📊 レーダーチャート", "📈 詳細グラフ", "🤖 AI診断", "📄 レポート"])
        
        with tab1:
            st.header("音声特徴レーダーチャート")
            
            # ダミーデータでレーダーチャート風の表示
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("音量", "85", "良好")
                st.metric("音量安定性", "75", "安定")
            with col2:
                st.metric("ピッチ安定性", "70", "やや不安定")
                st.metric("明瞭度", "90", "非常に良好")
            with col3:
                st.metric("音の豊かさ", "80", "豊か")
                st.metric("音の明るさ", "75", "明るい")
        
        with tab2:
            st.header("詳細分析グラフ")
            
            # サンプル波形表示
            chart_data = np.random.randn(100)
            st.line_chart(chart_data)
            
            st.caption("※ デモ版のため実際の音声波形ではありません")
        
        with tab3:
            st.header("AI診断結果")
            
            st.markdown(f"""
            <div class="result-box">
            <h3>{name}さんの音声診断結果</h3>
            
            <p><strong>総合評価: ⭐⭐⭐⭐☆ (4.0/5.0)</strong></p>
            
            <h4>✅ 良い点</h4>
            <ul>
            <li>音量が適切で、聞き取りやすい声です</li>
            <li>発音が明瞭で、言葉がはっきり伝わります</li>
            <li>声に豊かさがあり、表現力があります</li>
            </ul>
            
            <h4>⚠️ 改善ポイント</h4>
            <ul>
            <li>ピッチの安定性を向上させると、より説得力が増します</li>
            <li>話すスピードをもう少しゆっくりにすると良いでしょう</li>
            </ul>
            
            <h4>💡 改善のヒント（{purpose}向け）</h4>
            <ul>
            <li>腹式呼吸を意識して、安定した息の流れを作りましょう</li>
            <li>鏡の前で練習し、表情も意識すると声も良くなります</li>
            <li>毎日5分の音読練習で、確実に改善できます</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with tab4:
            st.header("レポートダウンロード")
            
            col1, col2 = st.columns(2)
            with col1:
                st.button("📥 PDFレポートをダウンロード", use_container_width=True)
            with col2:
                st.button("📧 メールで送信", use_container_width=True)
            
            st.info("※ デモ版のためダウンロード機能は動作しません")

# CTA セクション
st.markdown("---")
st.header("🎯 さらに詳しい分析をご希望の方へ")

col1, col2 = st.columns([2, 1])
with col1:
    st.info("""
    💡 **パーソナル音声診断（Zoom 30分）**では、
    - プロの音声トレーナーによる詳細分析
    - あなただけのカスタマイズされた練習メニュー
    - フォローアップサポート（1ヶ月）
    
    をご提供します！
    """)

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔗 詳細診断を申し込む（¥9,800）", type="primary", use_container_width=True):
        st.success("✨ お申し込みありがとうございます！")
        st.balloons()

# フッター
st.markdown("---")
st.caption("© 2024 音声診断システム - あなたの声をもっと魅力的に")