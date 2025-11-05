import streamlit as st
import pandas as pd
from database import get_translations

def app():
    st.header("📜 Translation History")
    hist = get_translations(st.session_state.user[0])
    if hist:
        df = pd.DataFrame(hist, columns=["Paragraf", "Çevirin", "Skor", "Tarih"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Henüz çeviri geçmişin yok.")
