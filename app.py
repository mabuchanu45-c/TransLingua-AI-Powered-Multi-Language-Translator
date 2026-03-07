import streamlit as st
from groq import Groq
import time

# ── Configuration ──────────────────────────────────────────────────────────────
# Get your free API key at: https://console.groq.com/keys
# Locally, add this to .streamlit/secrets.toml
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "your_fallback_key_here") 
client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.3-70b-versatile"

# ── Safe Generate Function ────────────────────────────────────────────────────
def safe_generate(prompt):
    retries = 3
    for i in range(retries):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=4096,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if "429" in str(e) or "rate_limit" in str(e).lower():
                time.sleep(10)
            else:
                raise e
    raise Exception("API rate limit reached. Please try again in a few seconds.")

# ── Supported Languages ───────────────────────────────────────────────────────
LANGUAGES = [
    "English", "Spanish", "French", "German", "Chinese (Simplified)",
    "Chinese (Traditional)", "Japanese", "Korean", "Hindi", "Arabic",
    "Portuguese", "Russian", "Italian", "Dutch", "Turkish",
    "Swedish", "Polish", "Thai", "Vietnamese", "Indonesian",
    "Greek", "Czech", "Romanian", "Hungarian", "Danish",
    "Finnish", "Norwegian", "Hebrew", "Malay", "Filipino",
    "Swahili", "Tamil", "Telugu", "Bengali", "Urdu",
    "Persian", "Ukrainian", "Catalan", "Croatian", "Serbian",
]

# ── Translation Function ─────────────────────────────────────────────────────
def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    prompt = (
        f"You are a professional translator. "
        f"Translate the following text from {source_lang} to {target_lang}. "
        f"Only return the translated text, nothing else. "
        f"Preserve the original formatting and tone.\n\n"
        f"Text to translate:\n{text}"
    )
    return safe_generate(prompt)


def detect_language(text: str) -> str:
    prompt = (
        f"Detect the language of the following text. "
        f"Only return the language name (e.g., 'English', 'Spanish', 'French'), nothing else.\n\n"
        f"Text:\n{text}"
    )
    return safe_generate(prompt)


# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TransLingua — AI Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    *, html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a40 40%, #24243e 100%);
    }

    .hero {
        text-align: center;
        padding: 2.5rem 1rem 1rem;
    }
    .hero h1 {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: .25rem;
        letter-spacing: -1px;
    }
    .hero p {
        color: #a0aec0;
        font-size: 1.1rem;
        font-weight: 400;
    }

    .glass-card {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.75rem;
        margin-bottom: 1rem;
        transition: all .3s ease;
    }
    .glass-card:hover {
        border-color: rgba(102,126,234,.35);
        box-shadow: 0 8px 32px rgba(102,126,234,.12);
    }

    .card-label {
        font-size: .8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #667eea;
        margin-bottom: .75rem;
    }

    .result-card {
        background: linear-gradient(135deg, rgba(102,126,234,.12), rgba(118,75,162,.12));
        backdrop-filter: blur(16px);
        border: 1px solid rgba(102,126,234,.25);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 1rem;
    }
    .result-card .label {
        font-size: .75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #667eea;
        margin-bottom: .5rem;
    }
    .result-card .text {
        font-size: 1.15rem;
        line-height: 1.7;
        color: #e2e8f0;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: .75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: .5px;
        transition: all .3s ease !important;
        box-shadow: 0 4px 15px rgba(102,126,234,.3) !important;
    }

    /* ── Selectbox & Text Area ──────────────────────────────────────────  */
    .stSelectbox > div > div,
    .stTextArea > div > div > textarea {
        background: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    .stSelectbox > div > div:focus-within,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        background: rgba(0, 0, 0, 0.6) !important;
    }
    ::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
        opacity: 1;
    }

    /* ── Scroll Behavior ─────────────────────────────────────────────────── */
    html {
        scroll-behavior: smooth;
    }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)


# ── Session State ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "source_lang" not in st.session_state:
    st.session_state.source_lang = "English"
if "target_lang" not in st.session_state:
    st.session_state.target_lang = "Spanish"
if "show_history" not in st.session_state:
    st.session_state.show_history = False


# ── Hero Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🌐 TransLingua</h1>
    <p>AI-Powered Multi-Language Translator · Powered by Groq & Llama 3.3</p>
</div>
""", unsafe_allow_html=True)

# ── Language Selectors ────────────────────────────────────────────────────────
col_src, col_swap, col_tgt = st.columns([5, 1, 5])

with col_src:
    src_idx = LANGUAGES.index(st.session_state.source_lang) if st.session_state.source_lang in LANGUAGES else 0
    source_language = st.selectbox(
        "Source Language",
        LANGUAGES,
        index=src_idx,
        key="src_select",
    )

with col_swap:
    if st.button("⇄", key="swap_btn"):
        st.session_state.source_lang, st.session_state.target_lang = (
            st.session_state.target_lang,
            st.session_state.source_lang,
        )
        st.rerun()

with col_tgt:
    tgt_idx = LANGUAGES.index(st.session_state.target_lang) if st.session_state.target_lang in LANGUAGES else 1
    target_language = st.selectbox(
        "Target Language",
        LANGUAGES,
        index=tgt_idx,
        key="tgt_select",
    )

st.session_state.source_lang = source_language
st.session_state.target_lang = target_language

# ── Input Area ────────────────────────────────────────────────────────────────
text = st.text_area(
    "Enter text to translate",
    height=180,
    placeholder="Type or paste your text here…",
)

# ── Buttons ───────────────────────────────────────────────────────────────────
col_translate, col_detect, col_clear, col_history = st.columns([1.5, 1.5, 1, 1])

with col_translate:
    translate_clicked = st.button("🚀 Translate", use_container_width=True)

with col_detect:
    detect_clicked = st.button("🔍 Detect", use_container_width=True)

with col_clear:
    clear_clicked = st.button("🗑️ Clear", use_container_width=True)

with col_history:
    if st.button("📜 History", key="history_toggle", use_container_width=True):
        st.session_state.show_history = not st.session_state.show_history
        st.rerun()

# ── Clear ─────────────────────────────────────────────────────────────────────
if clear_clicked:
    st.session_state.history = []
    st.rerun()

# ── Detect Language ───────────────────────────────────────────────────────────
if detect_clicked:
    if text.strip():
        with st.spinner("Detecting language..."):
            try:
                detected = detect_language(text)
                st.success(f"Detected: {detected}")
            except Exception as e:
                st.error(f"Detection failed: {str(e)}")

# ── Translate ─────────────────────────────────────────────────────────────────
if translate_clicked:
    if text.strip():
        with st.spinner("Translating..."):
            try:
                translated = translate_text(text, source_language, target_language)

                st.markdown(f"""
                <div class="result-card">
                    <div class="label">{source_language} → {target_language}</div>
                    <div class="text">{translated}</div>
                </div>
                """, unsafe_allow_html=True)

                st.session_state.history.insert(0,{
                    "source": text,
                    "result": translated,
                    "from": source_language,
                    "to": target_language
                })

            except Exception as e:
                st.error(f"Translation failed: {str(e)}")

# ── History ───────────────────────────────────────────────────────────────────
if st.session_state.show_history and st.session_state.history:
    st.markdown('<div id="history-section"></div>', unsafe_allow_html=True)
    st.markdown("### 📜 Recent Translations")

    for item in st.session_state.history[:10]:
        st.write(f"**{item['from']} → {item['to']}**")
        st.write("Original:", item["source"])
        st.write("Translated:", item["result"])
        st.write("---")