import streamlit as st
import pandas as pd
from database import get_translations, delete_translation

st.set_page_config(page_title="Geçmiş Çeviriler", page_icon="📜")

# --- Kullanıcı oturumu kontrolü
if "user" not in st.session_state:
    st.warning("⚠️ Lütfen önce giriş yapın.")
    st.stop()

st.title("📜 Geçmiş Çeviriler")

# --- Çeviri kayıtlarını getir
hist = get_translations(st.session_state.user[0])

if hist:
    st.write("### 🔍 Kayıtlı Çeviriler")

    for idx, (paragraph, user_translation, reference_translation, similarity, timestamp, record_id) in enumerate(hist):
        with st.expander(f"📄 {timestamp} — Skor: {similarity:.2f}"):
            st.markdown(f"**📝 Paragraf:** {paragraph}")
            st.markdown(f"**💬 Senin Çevirin:** {user_translation}")
            st.markdown(f"**📘 Referans Çeviri:** {reference_translation}")

            if st.button("🗑️ Sil", key=f"del_{record_id}"):
                delete_translation(record_id, st.session_state.user[0])
                st.success("✅ Kayıt silindi!")
                st.rerun()
else:
    st.info("Henüz çeviri geçmişin yok.")
