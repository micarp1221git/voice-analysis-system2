import streamlit as st
import time

# ページ設定
st.set_page_config(
    page_title="音声診断システム（デモ）",
    page_icon="🎤",
    layout="wide"
)

# タイトル
st.title("🎤 音声診断システム")
st.subheader("あなたの声を分析して、改善のヒントをお届けします")

# サイドバー
with st.sidebar:
    st.header("📊 システム情報")
    st.info("最大30秒の音声ファイルを分析します")
    st.success("✅ Streamlit動作確認OK！")

# メイン
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("お名前", value="田中太郎")
    purpose = st.selectbox("目的", ["話し声の印象", "歌", "プレゼン対策"])
    uploaded_file = st.file_uploader("音声ファイルをアップロード", type=['wav', 'mp3'])

with col2:
    st.info("📌 このデモ版では音声分析機能は動作しません")
    st.info("🎯 UIの確認用です")

if st.button("🔍 分析開始（デモ）", type="primary"):
    if uploaded_file:
        progress = st.progress(0)
        for i in range(100):
            progress.progress(i + 1)
            time.sleep(0.01)
        
        st.balloons()
        st.success("✅ デモ分析完了！")
        
        # 結果表示
        st.header("📊 分析結果（サンプル）")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("音量", "85", "良好")
        col2.metric("明瞭度", "90", "非常に良好")
        col3.metric("安定性", "75", "安定")
        
        st.info(f"""
        ### {name}さんの診断結果
        
        ✅ 音量が適切で聞き取りやすい声です
        ✅ 発音が明瞭で言葉がはっきり伝わります
        ⚠️ ピッチの安定性を向上させるとより良くなります
        
        **改善のヒント**: 腹式呼吸を意識しましょう
        """)
        
        if st.button("🔗 詳細診断を申し込む（¥9,800）", type="primary"):
            st.balloons()
            st.success("お申し込みありがとうございます！")
    else:
        st.error("ファイルをアップロードしてください")