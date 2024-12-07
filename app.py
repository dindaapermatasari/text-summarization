import streamlit as st
from summarizer import fetch_and_clean_article, summarize_text


st.set_page_config(page_title="📜 Text Summarization App", layout="wide")
st.title("📜 Text Summarization App")
st.markdown("Aplikasi untuk merangkum teks atau artikel.")


st.sidebar.header("⚙️ Pilih Metode Input")
option = st.sidebar.radio("Metode Input:", ["Manual", "URL Berita"])
st.sidebar.markdown("---")
st.sidebar.subheader("Pengaturan Ringkasan")
max_len = st.sidebar.slider("Panjang Maksimal Ringkasan", 100, 300, 150, step=10)
min_len = st.sidebar.slider("Panjang Minimal Ringkasan", 10, 100, 30, step=5)


if option == "Manual":
    input_text = st.text_area("Masukkan teks yang ingin dirangkum di sini:", height=200)
    input_url = None
elif option == "URL Berita":
    input_url = st.text_input("Masukkan URL artikel berita:")
    input_text = None


if st.button("🔍 Proses Ringkasan"):
    if option == "Manual" and input_text and input_text.strip():
        with st.spinner("Sedang merangkum teks..."):
            try:
                summary = summarize_text(
                    input_text, max_length=max_len, min_length=min_len
                )
                st.subheader("📋 Hasil Ringkasan:")
                st.success(summary)
                summary_length = len(summary.split())  # Menghitung jumlah kata
                st.info(f"📝 Panjang ringkasan: {summary_length} kata")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat merangkum teks: {e}")

    elif option == "URL Berita" and input_url and input_url.strip():
        with st.spinner("Mengambil artikel dari URL..."):
            try:
                article_text = fetch_and_clean_article(input_url)
                if article_text:
                    summary = summarize_text(
                        article_text, max_length=max_len, min_length=min_len
                    )
                    st.subheader("📋 Hasil Ringkasan:")
                    st.success(summary)
                    summary_length = len(summary.split())
                    st.info(f"📝 Panjang ringkasan: {summary_length} kata")
                else:
                    st.warning("Teks artikel kosong. Pastikan URL benar.")
            except Exception as e:
                st.error(
                    f"Terjadi kesalahan saat mengambil atau merangkum artikel: {e}"
                )
    else:
        st.warning("Silakan masukkan teks atau URL yang valid!")

st.markdown("---")
st.caption("Oleh Dinda Ayu Permatasari ❤️")
