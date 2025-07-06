import streamlit as st
import os
import random
import base64

# ページ設定
st.set_page_config(page_title="MachiColla Top", layout="wide")

# ランダム背景画像の読み込み
background_folder = "fortoppages"
image_files = [f for f in os.listdir(background_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

if image_files:
    selected_image_path = os.path.join(background_folder, random.choice(image_files))
    with open(selected_image_path, "rb") as f:
        bg_data = f.read()
    encoded_bg = base64.b64encode(bg_data).decode()

    # 背景画像として埋め込み
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_bg}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# タイトル画像の表示（1.5倍サイズ）
logo_path = "machicollatext.png"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_data = f.read()
    encoded_logo = base64.b64encode(logo_data).decode()

    st.markdown(
        f"""
        <div style="position: absolute; top: 12%; width: 100%; text-align: center;">
            <img src="data:image/png;base64,{encoded_logo}" style="width: 60%; max-width: 800px;" />
        </div>
        """,
        unsafe_allow_html=True
    )

# 🎨ボタン（画面下部中央・固定・クリックでリダイレクト）
st.markdown(
    """
    <style>
    .enter-btn {
        position: fixed;
        bottom: 5%;
        left: 50%;
        transform: translateX(-50%);
        background-color: #ff69b4;
        color: white;
        padding: 0.8em 2em;
        border: none;
        border-radius: 25px;
        font-size: 20px;
        cursor: pointer;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        z-index: 9999;
    }
    .enter-btn:hover {
        background-color: #ff1493;
        transform: translateX(-50%) scale(1.05);
    }
    </style>
    <button class="enter-btn" onclick="window.location.href='/app2'">🎨 Enter Gallery</button>
    """,
    unsafe_allow_html=True
)