import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
import gtts
from io import BytesIO
import os

# Directly configure the API key here
genai.configure(api_key="AIzaSyCmoyiLaXLT-dewnC3L7klTllJOyU49ImA")

prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 1000 words. Please provide the summary of the text given here: """

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        raise e

def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

def translate_summary(summary, target_language):
    translator = Translator()
    translated = translator.translate(summary, dest=target_language)
    return translated.text

def text_to_speech(text, language):
    tts = gtts.gTTS(text=text, lang=language)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

st.title("YouTube Transcript Summarizer")
youtube_link = st.text_input("Enter YouTube Video Link:")

languages = {
    "Telugu": "te",
    "Tamil": "ta",
    "Hindi": "hi",
    "Malayalam": "ml",
    "Bengali": "bn",
    "Kannada": "kn",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Marathi": "mr",
    "Oriya": "or",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Spanish": "es"
}

selected_languages = st.multiselect("Select languages for translation:", list(languages.keys()))

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Summarized Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
        if selected_languages:
            for language in selected_languages:
                translated_summary = translate_summary(summary, languages[language])
                st.markdown(f"## Detailed Notes in {language}:")
                st.write(translated_summary)
                audio_file = text_to_speech(translated_summary, languages[language])
                st.audio(audio_file, format="audio/mp3")
