import streamlit as st
from googletrans import Translator

translator = Translator()

indian_languages = {
    'Hindi': 'hi', 'English': 'en', 'Telugu': 'te', 'Tamil': 'ta', 'Marathi': 'mr',
    'Gujarati': 'gu', 'Kannada': 'kn', 'Malayalam': 'ml', 'Odia': 'or',
    'Punjabi': 'pa', 'Bengali': 'bn', 'Assamese': 'as', 'Urdu': 'ur', 'Sanskrit': 'sa'
}

def chatbot_response(user_input, target_lang_code='en'):
    try:
        detected_lang = translator.detect(user_input).lang
        response = "You said: " + user_input
        translated_response = translator.translate(response, src=detected_lang, dest=target_lang_code).text
        return translated_response
    except Exception as e:
        return f"Error: {e}"

st.title("Multilingual Indian Language Chatbot")

user_message = st.text_area("Enter your message (any Indian language):")

output_language = st.selectbox("Choose output language:", list(indian_languages.keys()), index=1)

if st.button("Translate"):
    if user_message:
        target_lang = indian_languages[output_language]
        result = chatbot_response(user_message, target_lang)
        st.write("Chatbot response:")
        st.write(result)
