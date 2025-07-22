import streamlit as st
import requests
import os
import zipfile
import io

# ==== CẤU HÌNH ====
API_KEY = "sk_68d451c059b232c8e8ff9d5ae0dc26088ef33d777a638e35"
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"
API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

headers = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}

# ==== GIAO DIỆN ====
st.set_page_config(page_title="Text to Voice – Bradford", layout="centered")
st.title("🎙️ Chuyển văn bản thành giọng nói (Bradford - ElevenLabs)")

text_input = st.text_area("📌 Nhập văn bản (mỗi dòng sẽ tạo 1 file .mp3):", height=200)

if st.button("🎧 Tạo file MP3"):
    lines = [line.strip() for line in text_input.strip().split("\n") if line.strip() != ""]

    if not lines:
        st.warning("Vui lòng nhập ít nhất 1 dòng văn bản.")
    else:
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for idx, line in enumerate(lines, 1):
                payload = {
                    "text": line,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.5
                    }
                }

                response = requests.post(API_URL, headers=headers, json=payload)
                if response.status_code == 200:
                    filename = f"{idx}.mp3"
                    zip_file.writestr(filename, response.content)
                    st.audio(response.content, format="audio/mp3")
                    st.success(f"✅ Đã tạo {filename}")
                else:
                    st.error(f"❌ Lỗi ở dòng {idx}: {response.text}")

        st.download_button(
            label="⬇️ Tải tất cả file MP3 (.zip)",
            data=zip_buffer.getvalue(),
            file_name="voice_outputs.zip",
            mime="application/zip"
        )
