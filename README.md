# Multilingual Chatbot

A premium, interactive Streamlit web application designed to bridge language barriers across India. The application provides seamless translation and transliteration between English and 13 major Indian languages, enriched with voice synthesis, an autocomplete IME, and an intelligent conversational chatbot powered by Google Gemini.

---

## 🌟 Key Features

### 1. Translation Module
*   **Direct Translator**: Translate text between English and 13 major Indian languages with word and character metrics, clear/reset buttons, and instant translations.
*   **Conversational Chatbot**: Engage in multi-turn translations and conversations. When configured with a free Gemini API key, the chatbot acts as a context-aware translation assistant that remembers history, adapts to language switches, and responses natively in the selected script.
*   **Text-to-Speech (TTS)**: Synthesize audio for translated outputs using `gTTS`. The native audio controls are completely hidden via custom CSS for a clutter-free interface, with a simple "Listen" button triggering immediate, smooth playback.

### 2. Transliteration Module
*   **Bulk Paragraph Converter**: Converts phonetic Roman script (English letters) into native Indian scripts instantly (e.g. typing "namaste" converts to "नमस्ते").
*   **Interactive Typist (IME)**: Provide a real-time autocomplete typing assistant. Fetch word-by-word suggestions from Google Input Tools API, allowing users to click autocomplete suggestion buttons to build sentences with Undo and Clear features.

### 3. Smart Chat Configuration
*   An optional input field in the sidebar allows you to securely paste a free Google Gemini API key (from Google AI Studio).
*   **Smart AI Mode**: Unlocks state-of-the-art LLM capabilities.
*   **Offline Mode**: Falls back to an upgraded regex word-boundary rule engine.

---

## 🛠️ Supported Languages

The application supports English and **13 major Indian languages**:
*   Hindi (हिन्दी)
*   Telugu (తెలుగు)
*   Tamil (தமிழ்)
*   Marathi (मराठी)
*   Gujarati (ગુજરાતી)
*   Kannada (ಕನ್ನಡ)
*   Malayalam (മലയാളം)
*   Bengali (বাংলা)
*   Punjabi (ਪੰਜਾਬੀ)
*   Odia (ଓଡ଼ିଆ)
*   Urdu (اردو)
*   Assamese (অসমীয়া)
*   Sanskrit (संस्कृत)

*Note: Speech synthesis (TTS) supports all major languages except Odia, Assamese, and Sanskrit due to engine constraints.*

---

## 🚀 Installation & Setup

### Prerequisites
*   Python 3.8 or higher
*   An internet connection (for Google Translate and Google Input Tools APIs)

### Steps

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd Multilingual-Chatbot
    ```

2.  **Create and Activate a Virtual Environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

---

## 💻 Running the Application

Launch the Streamlit server using:
```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`.

---

## 🔑 AI Configuration (Optional)

To enable the smart conversational assistant:
1.  Go to [Google AI Studio](https://aistudio.google.com/) and create a free Gemini API Key.
2.  Open the **Translation Module** tab, expand the sidebar, and paste your key under the **Smart Chat Configuration** section.
3.  The chatbot will immediately switch from offline rules to intelligent, context-aware translation and conversation.

---

## 🎨 Premium User Experience

*   **Responsive Layout**: Tailored CSS for custom cards, margins, badges, and fonts (using Google Outfit font).
*   **Auto Light/Dark Theme Support**: Glassmorphic styling adjusts cleanly between light and dark mode preferences.
*   **Compact Design**: Optimized header and card layouts to maximize workspace and improve readability.
