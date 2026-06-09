import streamlit as st
from deep_translator import GoogleTranslator
import urllib.request
import urllib.parse
import json
import streamlit.components.v1 as components

# Set page configurations
st.set_page_config(
    page_title="Multilingual Chatbot",
    page_icon="🔤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling
st.markdown("""
    <style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700;800&display=swap');
    
    /* Global styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Title font */
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Header Card */
    .header-banner {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #2563eb 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1.25rem;
        box-shadow: 0 6px 15px -4px rgba(124, 58, 237, 0.3);
    }
    
    .header-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }
    
    .header-subtitle {
        font-size: 0.9rem;
        font-weight: 400;
        opacity: 0.95;
        max-width: 800px;
        margin: 0 auto;
    }

    /* Custom container cards styling */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(255, 255, 255, 0.8);
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
    }
    
    /* Output Box */
    .output-box {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 1.25rem;
        font-size: 1.1rem;
        min-height: 150px;
        white-space: pre-wrap;
        color: #0f172a;
        box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
    }

    /* Metric Badges */
    .metric-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 500;
        background-color: #f1f5f9;
        color: #475569;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid #e2e8f0;
    }

    @media (prefers-color-scheme: dark) {
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: rgba(30, 41, 59, 0.7) !important;
            border-color: #334155 !important;
        }
        .output-box {
            background-color: #0f172a;
            border-color: #334155;
            color: #f8fafc;
        }
        .metric-badge {
            background-color: #334155;
            color: #cbd5e1;
            border-color: #475569;
        }
    }
    
    /* Interactive Suggestion Buttons */
    .stButton > button {
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
    }
    
    /* Hide native Streamlit audio players completely but keep functionality */
    div[data-testid="stAudio"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Indian language mappings
indian_languages = {
    'Hindi': 'hi',
    'English': 'en',
    'Telugu': 'te',
    'Tamil': 'ta',
    'Marathi': 'mr',
    'Gujarati': 'gu',
    'Kannada': 'kn',
    'Malayalam': 'ml',
    'Odia': 'or',
    'Punjabi': 'pa',
    'Bengali': 'bn',
    'Assamese': 'as',
    'Urdu': 'ur',
    'Sanskrit': 'sa'
}

# Source languages (including Auto Detect)
source_languages = {'Auto Detect': 'auto'}
source_languages.update(indian_languages)

# API helper for Google Input Tools Transliteration
def get_transliteration_suggestions(word, lang_code):
    if not word.strip():
        return []
    url = "https://inputtools.google.com/request"
    params = {
        "text": word,
        "itc": f"{lang_code}-t-i0-und",
        "num": 5,
        "cp": 0,
        "cs": 1,
        "ie": "utf-8",
        "oe": "utf-8",
        "app": "demopage"
    }
    try:
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data[0] == 'SUCCESS':
                return data[1][0][1]
        return [word]
    except Exception:
        return [word]

def transliterate_text(text, lang_code):
    if not text.strip():
        return ""
    words = text.split()
    transliterated_words = []
    for w in words:
        # Separate punctuation and handle the word
        clean_word = "".join(c for c in w if c.isalnum())
        if clean_word:
            suggestions = get_transliteration_suggestions(clean_word, lang_code)
            best_match = suggestions[0] if suggestions else clean_word
            
            # Find and restore prefix/suffix punctuation
            first_idx = w.find(clean_word)
            prefix = w[:first_idx]
            suffix = w[first_idx + len(clean_word):]
            transliterated_words.append(f"{prefix}{best_match}{suffix}")
        else:
            transliterated_words.append(w)
    return " ".join(transliterated_words)

# Conversational Chatbot Assistant Logic
def generate_bot_response(user_input, target_lang_code, api_key=None):
    import re
    import requests
    
    # If a Gemini API Key is provided, use the official free Gemini API for an intelligent conversational experience!
    if api_key and api_key.strip():
        try:
            # Map chat history to Gemini's format: {"role": "user"|"model", "parts": [{"text": "..."}]}
            contents = []
            for msg in st.session_state.chat_history:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": msg["content"]}]
                })
            
            # Map target lang code to full language name for system instruction context
            target_lang_name = "English"
            for name, code in indian_languages.items():
                if code == target_lang_code:
                    target_lang_name = name
                    break
            
            system_instruction = (
                f"You are a {target_lang_name} translation assistant.\n\n"
                f"- Translate any text the user gives you into {target_lang_name} immediately.\n"
                "- Do NOT ask clarifying questions if the target language is already known.\n"
                "- Do NOT repeat the original text back.\n"
                f"- Output the {target_lang_name} translation directly.\n"
                "- If the user changes the target language, switch and confirm once.\n"
                "- Default to full translation, not transliteration, unless asked."
            )
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key.strip()}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "systemInstruction": {
                    "parts": [{"text": system_instruction}]
                },
                "contents": contents
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=12)
            if response.status_code == 200:
                res_json = response.json()
                reply = res_json['candidates'][0]['content']['parts'][0]['text']
                return reply
            else:
                print(f"Gemini API Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Exception during Gemini API call: {e}")
            
    # Fallback/Offline Rule-Based Engine
    try:
        # Detect context by translating user message to English
        english_input = GoogleTranslator(source='auto', target='en').translate(user_input).lower()
    except Exception:
        english_input = user_input.lower()
        
    # Helper to check for whole words/phrases using boundaries
    def contains_any(pattern_list):
        for pattern in pattern_list:
            # Match word boundaries for safety
            if re.search(r'\b' + re.escape(pattern) + r'\b', english_input):
                return True
        return False

    # 1. Greetings
    if contains_any(["hello", "hi", "hey", "namaste", "vanakkam", "namaskaram", "yo", "sup", "greetings"]):
        reply = "Hello! I am your multilingual chatbot assistant. How can I help you today? You can translate text, transliterate phonetic words, or ask me questions."
    
    # 2. Help/Features
    elif contains_any(["help", "features", "capabilities", "what can you do", "skills", "function"]):
        reply = "I am an enhanced multilingual chatbot! I support two main modules:\n1. **Translation Module**: Translate text between English and 13 Indian languages, speak translations aloud, and converse with this chatbot.\n2. **Transliteration Module**: Convert phonetic Roman script into native scripts in real-time with autocomplete suggestions."
    
    # 3. How are you / status
    elif contains_any(["how are you", "how's it going", "how do you do", "how are u"]):
        reply = "I am doing great, thank you for asking! I'm ready to assist you with translation and transliteration. How can I help you today?"
        
    # 4. Identity / Name
    elif contains_any(["who are you", "what is your name", "your name", "introduce yourself"]):
        reply = "I am the Multilingual Chatbot Assistant, designed to help you communicate across Indian languages by translating and transliterating text easily."
        
    # 5. Supported languages
    elif contains_any(["languages", "support", "which language", "list"]):
        reply = "I support English and 13 major Indian languages: Hindi, Telugu, Tamil, Marathi, Gujarati, Kannada, Malayalam, Bengali, Punjabi, Odia, Urdu, Assamese, and Sanskrit."
        
    # 6. Gratitude
    elif contains_any(["thank", "thanks", "appreciate", "helpful"]):
        reply = "You're very welcome! I'm happy to help. Let me know if there's anything else you'd like to translate or transliterate!"
        
    # 7. Goodbyes
    elif contains_any(["bye", "goodbye", "see you", "exit", "quit"]):
        reply = "Goodbye! It was a pleasure assisting you. Have a wonderful day!"
        
    # 8. Jokes / Humor
    elif contains_any(["joke", "tell me a joke", "laugh"]):
        reply = "Why did the computer go to the doctor? Because it had a virus! 😄"
        
    # 9. Fallback response for questions or statements
    else:
        # Check if it looks like a question
        if "?" in user_input or any(q in english_input for q in ["what", "why", "how", "who", "where", "which"]):
            reply = f"I understand you have a question: '{user_input}'. As your multilingual assistant, I can translate this query or help you transliterate it into native scripts. What language would you like to translate it to?"
        else:
            reply = f"I understand you are saying: '{user_input}'. How can I help you with translating or transliterating this?"

    # If target is English, return directly
    if target_lang_code == 'en':
        return reply

    # Translate response back to the target language
    try:
        translated_reply = GoogleTranslator(source='en', target=target_lang_code).translate(reply)
        return translated_reply
    except Exception as e:
        return f"Error translating response: {e}\n\nEnglish response: {reply}"

# App Header
st.markdown("""
    <div class="header-banner">
        <div class="header-title">Multilingual Chatbot</div>
        <div class="header-subtitle">Your interactive gateway to Indian languages. Seamlessly translate and transliterate with advanced speech, conversational chat, and real-time autocomplete suggestions.</div>
    </div>
""", unsafe_allow_html=True)

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "translit_accumulated" not in st.session_state:
    st.session_state.translit_accumulated = ""
if "speak_text" not in st.session_state:
    st.session_state.speak_text = None
if "speak_lang" not in st.session_state:
    st.session_state.speak_lang = "en"
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = ""

# Sidebar navigation
st.sidebar.markdown("""
    <div style="text-align: center; padding-bottom: 1rem;">
        <span style="font-size: 4rem;">🌐</span>
        <h2 style="margin-top: 0.5rem; font-family: 'Outfit', sans-serif;">Navigation</h2>
    </div>
""", unsafe_allow_html=True)

module = st.sidebar.radio(
    "Choose Module:",
    ["Translation Module", "Transliteration Module"],
    index=0
)

# Optional Gemini API Key config
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔑 Smart Chat Configuration")
st.sidebar.text_input(
    "Gemini API Key (Optional):",
    value=st.session_state.get("gemini_api_key", ""),
    type="password",
    help="Get a free Gemini API key from Google AI Studio to unlock full conversational AI capability.",
    key="gemini_api_key"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Quick Tips")
if "Translation" in module:
    st.sidebar.info("""
        - **Direct Translator**: Enter text, choose target language and click 'Translate'.
        - **Chatbot Mode**: Speak with the chatbot naturally in any language.
        - **Text-to-Speech**: Click 🔊 to listen to translations.
    """)
else:
    st.sidebar.info("""
        - **Bulk Converter**: Paste romanized text and hit Transliterate.
        - **Interactive IME**: Type word-by-word. Click suggestions to build your sentence!
    """)

# --- MODULE 1: TRANSLATION ---
if module == "Translation Module":
    st.markdown("## Multilingual Translation Module")
    
    # Sub-tabs for Direct Translation & Chatbot
    tab_direct, tab_chat = st.tabs(["Direct Translator", "Conversational Chatbot"])
    
    # Direct Translator
    with tab_direct:
        with st.container(border=True):
            col1, col2 = st.columns(2)
            
            with col1:
                src_lang_name = st.selectbox("From Language:", list(source_languages.keys()), index=0, key="trans_src")
                input_text = st.text_area("Enter Text:", height=150, placeholder="Type your text here...", key="trans_input")
                
                # Word/Char metrics
                char_count = len(input_text)
                word_count = len(input_text.split()) if input_text.strip() else 0
                st.markdown(f'<span class="metric-badge">🔠 Characters: {char_count}</span><span class="metric-badge">📝 Words: {word_count}</span>', unsafe_allow_html=True)
                
                # Actions Row
                btn_col1, btn_col2, _ = st.columns([1, 1, 2])
                with btn_col1:
                    translate_btn = st.button("Translate", type="primary", use_container_width=True)
                with btn_col2:
                    clear_btn = st.button("Clear Text", key="clear_trans", use_container_width=True)
                    if clear_btn:
                        st.session_state.trans_input = ""
                        st.rerun() if hasattr(st, "rerun") else st.experimental_rerun()
                        
            with col2:
                target_lang_name = st.selectbox("To Language:", list(indian_languages.keys()), index=0, key="trans_target")
                
                # Translate Logic
                translated_result = ""
                if translate_btn and input_text.strip():
                    src_code = source_languages[src_lang_name]
                    target_code = indian_languages[target_lang_name]
                    
                    with st.spinner("Translating..."):
                        try:
                            translated_result = GoogleTranslator(source=src_code, target=target_code).translate(input_text)
                        except Exception as e:
                            translated_result = f"Error during translation: {e}"
                
                # Output container
                st.markdown("Translated Output:")
                st.markdown(f'<div class="output-box">{translated_result}</div>', unsafe_allow_html=True)
                
                # Output actions
                if translated_result and not translated_result.startswith("Error"):
                    act_col1, act_col2, _ = st.columns([1, 1, 2])
                    with act_col1:
                        if st.button("🔊 Listen", key="speak_direct", use_container_width=True):
                            st.session_state.speak_text = translated_result
                            st.session_state.speak_lang = indian_languages[target_lang_name]
                            st.rerun() if hasattr(st, "rerun") else st.experimental_rerun()
                    with act_col2:
                        # Informative instruction for copying
                        st.caption("Highlight text to copy.")

    # Conversational Chatbot
    with tab_chat:
        with st.container(border=True):
            st.markdown("### 💬 Chatbot Assistant")
            st.markdown("Speak with our helper assistant. Select a language below, type your message, and the assistant will converse in your target language!")
            
            chat_lang_name = st.selectbox("Chat Assistant Language:", list(indian_languages.keys()), index=0, key="chat_target_lang")
            chat_lang_code = indian_languages[chat_lang_name]
            
            # Show a tip if the Gemini API Key is missing
            if not st.session_state.get("gemini_api_key"):
                st.info("💡 **Smart Conversations**: The chatbot is currently in offline/rule-based mode. To enable smart AI conversations, get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/) and paste it in the sidebar!")
            
            # Display Chat History
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
                    if msg["role"] == "assistant":
                        if st.button("🔊 Listen", key=f"speak_chat_{msg['id']}"):
                            st.session_state.speak_text = msg["content"]
                            st.session_state.speak_lang = chat_lang_code
                            st.rerun() if hasattr(st, "rerun") else st.experimental_rerun()
                            
            # Chat Input
            if user_prompt := st.chat_input("Say something..."):
                # Add user message
                st.session_state.chat_history.append({"role": "user", "content": user_prompt, "id": len(st.session_state.chat_history)})
                with st.chat_message("user"):
                    st.write(user_prompt)
                    
                # Generate Bot response
                with st.spinner("Thinking..."):
                    bot_reply = generate_bot_response(user_prompt, chat_lang_code, st.session_state.get("gemini_api_key"))
                    
                # Add bot response
                st.session_state.chat_history.append({"role": "assistant", "content": bot_reply, "id": len(st.session_state.chat_history)})
                st.rerun() if hasattr(st, "rerun") else st.experimental_rerun()
                
            # Clear chat history button
            if st.session_state.chat_history:
                if st.button("🧹 Clear Chat History", type="secondary"):
                    st.session_state.chat_history = []
                    st.rerun() if hasattr(st, "rerun") else st.experimental_rerun()


# --- MODULE 2: TRANSLITERATION ---
elif module == "Transliteration Module":
    st.markdown("## Transliteration Module")
    
    # Sub-tabs for Bulk & Interactive IME
    tab_bulk, tab_ime = st.tabs(["Bulk Paragraph Converter", "Interactive Typist (IME)"])
    
    # Filter languages for transliteration (removing English)
    translit_langs = {k: v for k, v in indian_languages.items() if k != 'English'}
    
    # Bulk Paragraph Converter
    with tab_bulk:
        with st.container(border=True):
            col1, col2 = st.columns(2)
            
            with col1:
                bulk_lang_name = st.selectbox("Transliterate to script of:", list(translit_langs.keys()), index=0, key="bulk_target")
                bulk_input = st.text_area(
                    "Enter phonetic Roman/English text:",
                    height=150,
                    placeholder="Example: namaste, aap kaise hai? (Press Transliterate to convert)",
                    key="bulk_input_text"
                )
                
                # metrics
                char_count = len(bulk_input)
                word_count = len(bulk_input.split()) if bulk_input.strip() else 0
                st.markdown(f'<span class="metric-badge">🔠 Characters: {char_count}</span><span class="metric-badge">📝 Words: {word_count}</span>', unsafe_allow_html=True)
                
                btn_col1, btn_col2, _ = st.columns([1, 1, 2])
                with btn_col1:
                    translit_btn = st.button("Transliterate", type="primary", use_container_width=True)
                with btn_col2:
                    clear_bulk = st.button("Clear Input", key="clear_bulk", use_container_width=True)
                    if clear_bulk:
                        st.session_state.bulk_input_text = ""
                        st.rerun() if hasattr(st, "rerun") else st.experimental_rerun()
                        
            with col2:
                transliterated_result = ""
                if translit_btn and bulk_input.strip():
                    lang_code = translit_langs[bulk_lang_name]
                    with st.spinner("Converting script..."):
                        transliterated_result = transliterate_text(bulk_input, lang_code)
                
                st.markdown("Transliterated Output (Native Script):")
                st.markdown(f'<div class="output-box">{transliterated_result}</div>', unsafe_allow_html=True)
                
                if transliterated_result:
                    act_col1, _ = st.columns([1, 3])
                    with act_col1:
                        if st.button("🔊 Listen", key="speak_bulk", use_container_width=True):
                            st.session_state.speak_text = transliterated_result
                            st.session_state.speak_lang = translit_langs[bulk_lang_name]
                            st.rerun() if hasattr(st, "rerun") else st.experimental_rerun()
        
    # Interactive Word-by-Word IME
    with tab_ime:
        with st.container(border=True):
            st.markdown("### Real-time Word-by-Word Transliteration IME")
            st.markdown("Type a single word phonetically in Roman script. The system will load autocomplete suggestions. Click a suggestion or press enter to add it to your sentence.")
            
            ime_lang_name = st.selectbox("Target Script Language:", list(translit_langs.keys()), index=0, key="ime_target")
            ime_lang_code = translit_langs[ime_lang_name]
            
            col_type, col_accum = st.columns([2, 3])
            
            with col_type:
                current_word = st.text_input(
                    "Type word phonetically (e.g. 'shubh'):",
                    key="ime_word_input"
                )
                
                # Show suggestions
                if current_word.strip():
                    suggestions = get_transliteration_suggestions(current_word.strip(), ime_lang_code)
                    st.markdown("**Suggestions (Click to insert):**")
                    
                    # Render buttons for each suggestion
                    for idx, sugg in enumerate(suggestions[:5]):
                        if st.button(f"✨ {sugg}", key=f"sugg_btn_{idx}", use_container_width=True):
                            st.session_state.translit_accumulated += sugg + " "
                            st.session_state.ime_word_input = ""
                            st.rerun() if hasattr(st, "rerun") else st.experimental_rerun()
                else:
                    st.info("Start typing an English/Roman phonetic word to see native script suggestions here.")
                    
            with col_accum:
                # Inline function callback to update accumulated state
                def sync_accum():
                    st.session_state.translit_accumulated = st.session_state.accum_text_area
                    
                st.text_area(
                    "Accumulated Text (You can edit directly):",
                    value=st.session_state.translit_accumulated,
                    key="accum_text_area",
                    on_change=sync_accum,
                    height=150
                )
                
                col_actions = st.columns(4)
                with col_actions[0]:
                    if st.button("🔊 Listen", key="speak_ime", use_container_width=True):
                        if st.session_state.translit_accumulated.strip():
                            st.session_state.speak_text = st.session_state.translit_accumulated
                            st.session_state.speak_lang = ime_lang_code
                            st.rerun() if hasattr(st, "rerun") else st.experimental_rerun()
                with col_actions[1]:
                    if st.button("↩️ Undo", key="undo_ime", use_container_width=True):
                        words = st.session_state.translit_accumulated.strip().split()
                        if words:
                            st.session_state.translit_accumulated = " ".join(words[:-1]) + " "
                        st.rerun() if hasattr(st, "rerun") else st.experimental_rerun()
                with col_actions[2]:
                    if st.button("🧹 Clear", key="clear_ime", use_container_width=True):
                        st.session_state.translit_accumulated = ""
                        st.rerun() if hasattr(st, "rerun") else st.experimental_rerun()
                with col_actions[3]:
                    st.caption("Highlight text to copy.")


# --- Audio Speech Synthesis Runner ---
# Generates and plays audio using gTTS (Google Text-to-Speech)
if st.session_state.speak_text:
    supported_gtts_langs = ['hi', 'te', 'ta', 'mr', 'gu', 'kn', 'ml', 'pa', 'bn', 'ur', 'en']
    lang_code = st.session_state.speak_lang
    
    if lang_code not in supported_gtts_langs:
        st.error(f"Audio synthesis is not supported for this language ({lang_code}) in gTTS.")
    else:
        try:
            from gtts import gTTS
            import io
            
            with st.spinner("Synthesizing audio..."):
                tts = gTTS(text=st.session_state.speak_text, lang=lang_code, slow=False)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                audio_bytes = fp.getvalue()
                
                # Render audio player with autoplay enabled (will be hidden by CSS)
                st.audio(audio_bytes, format="audio/mp3", autoplay=True)
        except Exception as e:
            st.error(f"Failed to generate speech: {e}")
            
    # Reset the flag so speech is not repeated on next rerun
    st.session_state.speak_text = None
