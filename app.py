import streamlit as st
import requests
import os
import zipfile
import io
import json

# ======= QUẢN LÝ API =======
API_KEYS_FILE = "api_keys.json"
MAX_WORDS_PER_KEY = 10000

def load_keys(path=API_KEYS_FILE):
    with open(path, "r") as f:
        return json.load(f)

def save_keys(keys, path=API_KEYS_FILE):
    with open(path, "w") as f:
        json.dump(keys, f, indent=2)

def select_available_key(max_words=MAX_WORDS_PER_KEY):
    keys = load_keys()
    for i, key in enumerate(keys):
        if key["used"] < max_words:
            return key["key"], i
    raise Exception("❌ Không còn API Key nào khả dụng.")

def increment_key_usage(index, words, path=API_KEYS_FILE):
    keys = load_keys(path)
    keys[index]["used"] += words
    save_keys(keys, path)

# ======= GIAO DIỆN =======
st.set_page_config(page_title="TTS - Bradford", layout="centered")

# ==== CSS giao diện đẹp hiện đại ====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background-color: #f2f4f8;
}

.container {
    background-color: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-top: 30px;
}

textarea {
    font-size: 16px !important;
    border-radius: 8px !important;
}

.stButton button {
    background-color: #2ecc71;
    color: white;
    padding: 0.5em 1.5em;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    margin-top: 10px;
}

.stDownloadButton button {
    border: 2px solid #27ae60;
    background-color: white;
    color: #27ae60;
    border-radius: 8px;
    padding: 0.5em 1.5em;
    font-size: 15px;
    margin-top: 10px;
}

footer {
    margin-top: 40px;
    color: #888;
    font-size: 14px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ==== NỘI DUNG CHÍNH ====
st.markdown('<div class="container">', unsafe_allow_html=True)

st.title("🎙️ Text to Speech – Giọng Bradford (ElevenLabs)")
st.markdown("💬 Chuyển mỗi dòng văn bản thành giọng nói `.mp3` sử dụng ElevenLabs (Bradford voice).")

text_input = st.text_area("✍️ Nhập vào văn bản cần chuyển đổi...", height=200)

if st.button("▶️ Tạo Giọng Nói"):
    lines = [line.strip() for line in text_input.strip().split("\n") if line.strip()]
    if not lines:
        st.warning("⚠️ Vui lòng nhập ít nhất 1 dòng văn bản.")
    else:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for idx, line in enumerate(lines, 1):
                word_count = len(line.strip().split())
                try:
                    api_key, key_index = select_available_key()
                except Exception as e:
                    st.error(str(e))
                    break

                headers = {
                    "xi-api-key": api_key,
                    "Content-Type": "application/json"
                }

                payload = {
                    "text": line,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.5
                    }
                }

                response = requests.post(
                    "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL",
                    headers=headers,
                    json=payload
                )

                if response.status_code == 200:
                    filename = f"{idx}.mp3"
                    zip_file.writestr(filename, response.content)
                    st.audio(response.content, format="audio/mp3")
                    st.success(f"✅ Dòng {idx} đã tạo thành công")
                    increment_key_usage(key_index, word_count)
                else:
                    st.error(f"❌ Lỗi ở dòng {idx}: {response.status_code} – {response.text}")
                    break

        st.download_button(
            label="⬇️ Tải MP3",
            data=zip_buffer.getvalue(),
            file_name="voice_outputs.zip",
            mime="application/zip"
        )

st.markdown('</div>', unsafe_allow_html=True)

# ==== CHÂN TRANG ====
st.markdown("""
<footer>
👨‍💻 Phát triển bởi <strong>Vinh Bảo</strong> – 2025
</footer>
""", unsafe_allow_html=True)
