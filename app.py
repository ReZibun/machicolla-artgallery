import streamlit as st
import os
import random
import base64
from dotenv import load_dotenv
from supabase import create_client

# ページ設定
st.set_page_config(page_title="MachiColla", layout="wide", initial_sidebar_state="collapsed")

# セッションで状態管理
if "page" not in st.session_state:
    st.session_state.page = "top"

# --------------------
# 関数：トップページ
# --------------------
def show_top():
    background_folder = "fortoppages"
    image_files = [f for f in os.listdir(background_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if image_files:
        selected_image_path = os.path.join(background_folder, random.choice(image_files))
        with open(selected_image_path, "rb") as f:
            encoded_bg = base64.b64encode(f.read()).decode()
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
            unsafe_allow_html=True
        )

    if os.path.exists("machicollatext.png"):
        with open("machicollatext.png", "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <div style="position: absolute; top: 12%; width: 100%; text-align: center;">
                <img src="data:image/png;base64,{logo_data}" style="width: 60%; max-width: 800px;" />
            </div>
            """,
            unsafe_allow_html=True
        )

    # HTMLボタンスタイルだけ追加（実際のボタンはst.buttonで処理）
    st.markdown("""
    <style>
    div[data-testid="stButton"] > button {
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
        font-weight: bold;
        cursor: pointer;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        z-index: 9999;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #ff1493;
        transform: translateX(-50%) scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# 通常通りst.buttonを呼び出す（位置はCSSが決める）
    if st.button("🎨 Enter Gallery", key="gallery-btn"):
        st.session_state.page = "gallery"
        st.rerun()

def show_gallery():
    import time
    import base64

    if "gallery_loaded" not in st.session_state:
        st.session_state.gallery_loaded = False

    if not st.session_state.gallery_loaded:
        # ロゴ画像をbase64エンコード
        with open("rez_color_logo2.png", "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()

        # HTML + CSSで中央配置 & 背景白
        st.markdown(f"""
        <style>
        .stApp {{
            background-color: white;
        }}
        .logo-center {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
        }}
        </style>
        <div class="logo-center">
            <img src="data:image/png;base64,{logo_base64}" width="300">
            <h3>Loading Gallery...</h3>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(1.5)
        st.session_state.gallery_loaded = True
        st.rerun()  # ✅ Streamlit v1.33以降
        return

    # 通常のギャラリー表示フェーズ
    load_dotenv()
    supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    storage_url = os.getenv("SUPABASE_STORAGE_URL")

    # ヘッダー画像＋ロゴ（上部）
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

    # Supabaseからデータ取得
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
                st.image(f"{storage_url}/{artwork['image_path']}", use_container_width=True)
                if artwork.get("description"):
                    st.markdown("**作品に込めた想い**")
                    st.write(artwork["description"])


# --------------------
# 表示切り替え
# --------------------
if st.session_state.page == "top":
    show_top()
elif st.session_state.page == "gallery":
    show_gallery()