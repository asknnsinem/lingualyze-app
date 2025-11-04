import streamlit as st
from database import add_user, get_user

def login_ui():
    st.title("🔐 Giriş / Kayıt")
    tab1, tab2 = st.tabs(["Giriş Yap", "Kayıt Ol"])

    with tab1:
        username = st.text_input("Kullanıcı Adı")
        password = st.text_input("Şifre", type="password")
        if st.button("Giriş"):
            user = get_user(username, password)
            if user:
                st.session_state.user = user
                st.success("✅ Giriş başarılı!")
                st.rerun()
            else:
                st.error("❌ Hatalı kullanıcı adı veya şifre")

    with tab2:
        new_user = st.text_input("Yeni Kullanıcı Adı")
        new_pass = st.text_input("Yeni Şifre", type="password")
        if st.button("Kayıt Ol"):
            try:
                add_user(new_user, new_pass)
                st.success("🎉 Kayıt başarılı! Giriş yapabilirsiniz.")
            except:
                st.warning("⚠️ Bu kullanıcı adı zaten mevcut.")

    st.stop()
