import streamlit as st
import pandas as pd

def convert_drive_url(url):
    if not isinstance(url, str):
        return None
    url = url.strip()

    if "drive.google.com" in url:
        if "/file/d/" in url:
            try:
                file_id = url.split("/file/d/")[1].split("/")[0]
                return file_id
            except Exception:
                return None
        elif "open?id=" in url:
            try:
                file_id = url.split("open?id=")[1].split("&")[0]
                return file_id
            except Exception:
                return None
    return None

# GoogleフォームのCSV読み込み
df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vT13dyy2yobEUq8gsBZp0BWzWY2YttwGmYmmm3DorjqwBRvgCtQCkJMJIWYCGFLV95gbEMFexAyPjJZ/pub?output=csv")

# 列名を短く変換
df.rename(columns={
    'アーティスト名\n(例：ガッチャマン)': 'アーティスト名',
    '作品名（テーマ）\n例：\n・将来の自分へ\n・これから読みたい本への気持ちを栞に\n・今隣の人が考えてそうなこと': '作品名（テーマ）',
    '何か伝えたいことがあればこちらに！': '伝えたいこと',
    '制作年月日': '制作年月日',
    '作品の写真': '作品の写真'
}, inplace=True)

# タイトル
st.title("みんなのアートギャラリー")

# 各作品を表示
for _, row in df.iterrows():
    st.subheader(row['作品名（テーマ）'])
    st.text(f"アーティスト名: {row['アーティスト名']}")

    file_id = convert_drive_url(row['作品の写真'].strip())

    if file_id is None:
        st.error("❌ 画像リンクの変換に失敗しました。URL形式を確認してください。")
    else:

        # iframeで画像埋め込み表示
        iframe_html = f"""
        <iframe src="https://drive.google.com/file/d/{file_id}/preview" width="100%" height="480" allow="autoplay"></iframe>
        """
        st.markdown(iframe_html, unsafe_allow_html=True)

    st.markdown("---")