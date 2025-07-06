import streamlit as st
import os
import base64
from dotenv import load_dotenv
from supabase import create_client, Client
import pandas as pd

# --------------------
# 環境変数の読み込み
# --------------------
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_STORAGE_URL = os.getenv("SUPABASE_STORAGE_URL")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --------------------
# ページ設定
# --------------------
st.set_page_config(
    page_title="MachiColla Gallery",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------
# ヘッダー画像の表示（存在確認つき）
# --------------------
with open("header-artgallery.jpeg", "rb") as f:
    header_encoded = base64.b64encode(f.read()).decode()

with open("machicollatext.png", "rb") as f:
    text_encoded = base64.b64encode(f.read()).decode()

st.markdown(
    f"""
    <style>
    .header-container {{
        position: relative;
        width: 100%;
    }}
    .header-image {{
        width: 150%;
        height: auto;
        display: block;
    }}
    .text-overlay {{
        position: absolute;
        top: 12%;
        left: 50%;
        transform: translate(-50%, -10%);
        z-index: 2;
        width: 40%;
        max-width: 100px;
    }}
    </style>
    <div class="header-container">
        <img src="data:image/png;base64,{text_encoded}" class="text-overlay">
        <img src="data:image/jpeg;base64,{header_encoded}" class="header-image">
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------
# Supabaseからデータ取得
# --------------------
response = supabase.table("artworks").select("*").eq("is_approved", True).order("created_at", desc=True).execute()
data = response.data

if not data:
    st.info("まだ承認された作品がありません。")
else:
    cols = st.columns(3)
    for i, artwork in enumerate(data):
        with cols[i % 3]:
            st.markdown(f"### {artwork.get('title', 'Untitled')}")
            st.markdown(f"**{artwork.get('artist_name', 'Unknown')}**")

            # 画像URL組み立て
            image_url = f"{SUPABASE_STORAGE_URL}/{artwork['image_path']}"
            st.image(image_url, use_container_width=True)

            # 作品に込めた想い（descriptionカラム）
            description = artwork.get("description", "")
            if description:
                st.markdown("**作品に込めた想い**")
                st.write(description)

