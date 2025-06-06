import streamlit as st
import pandas as pd
import os
import random

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")  # サイドバーを初期で折りたたみ

# セッション状態の初期化
if "show_main" not in st.session_state:
    st.session_state.show_main = False

# GoogleドライブURLからファイルIDを抽出
def convert_drive_url(url):
    if not isinstance(url, str):
        return None
    url = url.strip()
    if "drive.google.com" in url:
        if "/file/d/" in url:
            try:
                return url.split("/file/d/")[1].split("/")[0]
            except Exception:
                return None
        elif "open?id=" in url:
            try:
                return url.split("open?id=")[1].split("&")[0]
            except Exception:
                return None
    return None

# データの読み込みと整形
df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vT13dyy2yobEUq8gsBZp0BWzWY2YttwGmYmmm3DorjqwBRvgCtQCkJMJIWYCGFLV95gbEMFexAyPjJZ/pub?output=csv")

df.rename(columns={
    'アーティスト名\n(例：ガッチャマン)': 'アーティスト名',
    '作品名（テーマ）\n例：\n・将来の自分へ\n・これから読みたい本への気持ちを栞に\n・今隣の人が考えてそうなこと': '作品名（テーマ）',
    '作品に込めた想い・一押しポイント\n例：\n・将来たくさんのことに挑戦したいという思いから様々な色を使って違和感を表現しました！\n・今のなんかモヤモヤする気持ちを表現してみました': '作品の想い',
    '作品の写真': '作品の写真',
    '何か伝えたいことがあればこちらに！': '伝えたいこと',
    '制作年月日': '制作年月日'
}, inplace=True)

# トップページ
if not st.session_state.show_main:
    st.markdown("<style>body {background-color: black;}</style>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white;'>Welcome to Our Museum</h1>", unsafe_allow_html=True)

    image_folder = "fortoppages"
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(".jpg") or f.lower().endswith(".jpeg")]

    if image_files:
        selected_image = random.choice(image_files)
        st.image(os.path.join(image_folder, selected_image), use_container_width=True)

    st.markdown("""
        <style>
        div.stButton > button:first-child {
            font-size: 28px;
            padding: 20px 60px;
            background-color: white;
            color: black;
            border-radius: 10px;
            font-weight: bold;
            cursor: pointer;
            display: block;
            margin: 0 auto;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Enter Gallery"):
            st.session_state.show_main = True
            st.rerun()

    st.stop()

# ギャラリーページ
st.markdown('<a name="top"></a>', unsafe_allow_html=True)
st.image("header-artgallery.jpeg", use_container_width=True)
st.title("Machi Colla Art Gallery")

st.markdown("""
    <script>
    window.onload = function() {
        window.scrollTo(0, 0);
    }
    </script>
""", unsafe_allow_html=True)

# トップへ戻るボタン
st.markdown("""
    <style>
    .top-button {
        position: fixed;
        bottom: 40px;
        right: 40px;
        background-color: rgba(0,0,0,0.4);
        color: white;
        padding: 10px 18px;
        border-radius: 25px;
        text-decoration: none;
        font-size: 16px;
        z-index: 1000;
        transition: background-color 0.3s ease;
    }
    .top-button:hover {
        background-color: rgba(0,0,0,0.7);
    }
    </style>
    <a href="#top" class="top-button">▲ Top</a>
""", unsafe_allow_html=True)

# サイドバー（デフォルト閉じる）
with st.sidebar.expander("🔍 作者でジャンプ", expanded=False):
    unique_artists = df['アーティスト名'].dropna().unique()
    for artist in unique_artists:
        anchor = artist.replace(" ", "_").replace("\n", "").strip()
        st.markdown(f"[{artist}](#{anchor})")

# 各作品の表示
for _, row in df.iterrows():
    anchor = row['アーティスト名'].replace(" ", "_").replace("\n", "").strip()
    st.markdown(f"<a name='{anchor}'></a>", unsafe_allow_html=True)

    st.subheader(row['作品名（テーマ）'])
    st.text(f"アーティスト名: {row['アーティスト名']}")

    file_id = convert_drive_url(row['作品の写真'].strip())
    if file_id:
        st.markdown(f"""
            <iframe src="https://drive.google.com/file/d/{file_id}/preview" width="100%" height="480" allow="autoplay"></iframe>
        """, unsafe_allow_html=True)
    else:
        st.error("❌ 画像リンクの変換に失敗しました。URL形式を確認してください。")

    if '作品の想い' in row and pd.notna(row['作品の想い']) and row['作品の想い'].strip():
        st.markdown(f"**作品に込めた想い：** {row['作品の想い']}")

    st.markdown("---")