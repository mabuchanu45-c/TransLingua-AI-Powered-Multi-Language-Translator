# 🌐 TransLingua: AI-Powered Multi-Language Translator

TransLingua is a premium, high-performance translation application built with **Streamlit** and **Groq**. It delivers blazing-fast translations using the **Llama 3.3 70B** model.

## ✨ Features
- **40+ Languages** — English, Spanish, French, German, Chinese, Japanese, Korean, Hindi, Arabic, and many more.
- **Groq AI** — Powered by Llama 3.3 70B for blazing fast and accurate results.
- **Instant Detection** — Automatically detects the source language.
- **History Scroll** — One-tap scroll button to jump straight to your previous translations.
- **Swap Languages** — One-click language swap button (⇄).
- **Premium UI** — Modern dark theme with glassmorphism and smooth animations.

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- A Groq API Key (Get one at [console.groq.com](https://console.groq.com))

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/mabuchanu45-c/TransLingua.git
   cd TransLingua
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App
```bash
streamlit run app.py
```

## ⚙️ Configuration
The app uses Streamlit secrets for the API key. Create a `.streamlit/secrets.toml` file locally:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

## 📄 License
This project is open-source and available under the MIT License.
