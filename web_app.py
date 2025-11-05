import streamlit as st
import pandas as pd
import random, time
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
from database import init_db, save_translation
from utils import load_model, compute_score
from auth import login_ui

st.set_page_config(page_title="Lingualyze", page_icon="💬")
st.title("💬**Lingualyze**")
st.caption("Master languages through smart translation practice.")
# --- Başlat
init_db()
if "user" not in st.session_state:
    login_ui()

model = load_model()

st.set_page_config(page_title="Çeviri Alıştırması", page_icon="🌍")
st.title(f"🌍 Hoş geldin, {st.session_state.user[1]}!")

# --- Paragraf seçimi
df = pd.read_excel("paragraph.xlsx")
levels = df["seviye"].unique()
selected_level = st.selectbox("Seviyeni Seç:", levels)

if st.button("🎲 Paragraf Getir"):
    row = df[df["seviye"] == selected_level].sample(1).iloc[0]
    st.session_state.paragraph = row["paragraf"]
    st.session_state.reference = row["translate"]
    st.session_state.start_time = int(time.time())
    st.session_state.finished = False
    st.session_state.user_text = ""

# --- Paragraf göster
if "paragraph" in st.session_state:
    paragraph = st.session_state.paragraph
    ref = st.session_state.reference
    st.subheader("📝 Paragraf")
    st.write(paragraph)

    # Süre hesaplama
    words = len(paragraph.split())
    time_limit = max(30, int(words * 1.5))
    end_time = st.session_state.start_time + time_limit

    # 🔹 Akıcı HTML tabanlı sayaç
    st.components.v1.html(f"""
        <div style="font-size:18px;color:#90CAF9;margin-bottom:10px;">
            ⏳ Süre: <span id="timer">{time_limit}</span> saniye
        </div>
        <script>
        const end = {end_time} * 1000;
        const el = document.getElementById("timer");
        const update = () => {{
            const now = new Date().getTime();
            const diff = Math.max(0, Math.floor((end - now) / 1000));
            el.textContent = diff;
            if(diff > 0) requestAnimationFrame(update);
        }};
        update();
        </script>
    """, height=50)

    # Çeviri alanı
    st.session_state.user_text = st.text_area("💬 Çevirini Yaz", value=st.session_state.user_text)
    send = st.button("📤 Yolla")

    if int(time.time()) >= end_time or send:
        text = st.session_state.user_text.strip()
        if text:
            score = compute_score(model, ref, text)
            st.metric("Genel Skor", f"{score}")
            save_translation(st.session_state.user[0], paragraph, text, ref, score)

            st.markdown("---")
            st.subheader("🔍 Karşılaştırma")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**💬 Senin Çevirin:**")
                st.markdown(
                    f"<div style='background-color:#1E1E1E;padding:10px;border-radius:10px;'>{text}</div>",
                    unsafe_allow_html=True,
                )
            with col2:
                st.markdown("**📘 Referans Çeviri:**")
                st.markdown(
                    f"<div style='background-color:#1E1E1E;padding:10px;border-radius:10px;'>{ref}</div>",
                    unsafe_allow_html=True,
                )

            
        else:
            st.warning("⚠️ Çeviri alanı boş olamaz.")
