import streamlit as st
from deep_translator import GoogleTranslator

# Mapping of Indian language names to language codes
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
def chatbot_response(user_input, target_lang_code='en'):
    try:
        # Translate only the user's message
        translated_response = GoogleTranslator(source='auto', target=target_lang_code).translate(user_input)
        return translated_response
    except Exception as e:
        return f"Error: {e}"


st.title("Multilingual Indian Language Chatbot")

user_message = st.text_area("Enter your message (any Indian language):")

output_language = st.selectbox("Choose output language:", list(indian_languages.keys()), index=1)

if st.button("Translate"):
    if user_message.strip():
        target_lang = indian_languages.get(output_language, 'en')
        result = chatbot_response(user_message, target_lang)
        st.write("Chatbot response:")
        st.write(result)
    else:
        st.write("Please enter a message to translate.")

