import streamlit as st
import pandas as pd
from database import add_word, get_wordbook
from googletrans import Translator

st.set_page_config(page_title="WordList", page_icon="📘")

if "user" not in st.session_state:
    st.warning("⚠️ Lütfen önce giriş yapın.")
    st.stop()

st.title("📘 WordList")

translator = Translator()

st.markdown("### ➕ Yeni Kelime Ekle")
col1, col2, col3 = st.columns([1, 2, 2])

with col1:
    new_word = st.text_input("Kelime")

# 🔹 Otomatik çeviri işlemi
translation_result = ""
if new_word.strip():
    try:
        result = translator.translate(new_word, src="en", dest="tr")
        translation_result = result.text
    except Exception as e:
        translation_result = "(çeviri alınamadı)"

with col2:
    st.text_input("Otomatik Çeviri (EN→TR)", value=translation_result, disabled=True)

with col3:
    note = st.text_input("Not (isteğe bağlı)")

# 🔹 Veritabanına kaydet
if st.button("Ekle"):
    if new_word.strip():
        add_word(
            st.session_state.user[0],
            new_word,
            f"{translation_result} - {note}" if note else translation_result,
        )
        st.success(f"✅ '{new_word}' kelimesi WordList'e eklendi!")
        st.rerun()
    else:
        st.warning("⚠️ Kelime alanı boş olamaz.")

st.markdown("### 📚 Kayıtlı Kelimeler")
words = get_wordbook(st.session_state.user[0])
if words:
    df_words = pd.DataFrame(words, columns=["Kelime", "Not", "Tarih"])
    st.dataframe(df_words, use_container_width=True)
else:
    st.info("WordList boş.")
