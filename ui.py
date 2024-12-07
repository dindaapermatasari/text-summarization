from summarizer import fetch_and_clean_article
import streamlit as st


def render_sidebar():
    """Fungsi untuk membuat sidebar UI."""
    st.sidebar.header("⚙️ **Pengaturan**")
    st.sidebar.markdown("---")

    theme_mode = st.sidebar.selectbox("🌗 **Mode Tema**", ["Terang", "Gelap"])

    input_mode = st.sidebar.radio(
        "📥 **Pilih Metode Input**", ("Masukkan Teks Manual", "URL Berita")
    )

    st.sidebar.markdown("### 📏 **Panjang Ringkasan**")
    max_len = st.sidebar.slider("Panjang Maksimal", 50, 300, 150, 10)
    min_len = st.sidebar.slider("Panjang Minimal", 10, 100, 30, 5)
    st.sidebar.markdown("---")
    st.sidebar.info(
        "💡 **Tips**: Panjang ringkasan yang optimal tergantung pada kompleksitas teks."
    )
    return theme_mode, input_mode, max_len, min_len


def render_main_ui(input_mode):
    """Fungsi untuk membuat antarmuka utama."""
    st.title("📜 **Text Summarization App**")
    st.markdown(
        """
        **Selamat datang di aplikasi peringkas teks otomatis!**  
        Aplikasi ini akan membantu Anda merangkum artikel atau teks panjang dengan mudah menggunakan AI.
    """
    )

    input_text, url = "", None

    if input_mode == "Masukkan Teks Manual":
        st.markdown("### 📝 **Masukkan teks**")
        input_text = st.text_area("Silakan tempel teks Anda di sini:", height=200)
    elif input_mode == "URL Berita":
        st.markdown("### 🔗 **Masukkan URL Berita**")
        url = st.text_input("Masukkan URL artikel berita untuk dirangkum:")

    st.markdown("---")
    st.markdown("🚀 **Klik tombol Rangkum untuk memulai!**")
    return input_text, url


def display_summary(summary):
    """Fungsi untuk menampilkan hasil ringkasan."""
    if summary:
        st.subheader("📋 **Ringkasan:**")
        st.success(summary)
    else:
        st.warning("⚠️ Tidak dapat menghasilkan ringkasan. Silakan coba lagi.")


def apply_theme(theme_mode):
    """Fungsi untuk mengatur tema aplikasi."""
    if theme_mode == "Gelap":
        dark_theme_css = """
        <style>
        body {
            background-color: #2E2E2E;
            color: white;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        </style>
        """
        st.markdown(dark_theme_css, unsafe_allow_html=True)
    else:
        light_theme_css = """
        <style>
        body {
            background-color: white;
            color: black;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        </style>
        """
        st.markdown(light_theme_css, unsafe_allow_html=True)


def main():
    """Fungsi utama untuk menjalankan aplikasi."""
    theme_mode, input_mode, max_len, min_len = render_sidebar()
    apply_theme(theme_mode)
    input_text, url = render_main_ui(input_mode)

    if st.button("Rangkum", key="summarize_button"):
        summary = None

        if input_text:
            summary = f"Ringkasan teks: {input_text[:50]}..."
        elif url:
            article_text = fetch_and_clean_article(url)
            if article_text:
                summary = f"Ringkasan artikel: {article_text[:50]}..."
        else:
            st.warning("⚠️ Tidak dapat mengambil teks dari URL. Silakan coba lagi.")

        display_summary(summary)


if __name__ == "__main__":
    main()
