import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from googletrans import Translator
import gtts
from io import BytesIO
import re
st.set_page_config(
    page_title="YouTube Transcript Summarizer",  # Title of the web page
    page_icon="favicon.ico",  # Favicon file
    layout="centered"  # You can set the layout as "wide" or "centered"
)

# Configure the Generative AI API key
genai.configure(api_key="AIzaSyCmoyiLaXLT-dewnC3L7klTllJOyU49ImA")

# Prompt for summarization
prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 5000 words. Please provide the summary of the text given here: """

# Extract transcript details if available
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except TranscriptsDisabled:
        return None
    except Exception as e:
        st.error(f"Error while fetching transcript: {str(e)}")
        return None

# Generate content using generative AI model

def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    
    # Remove asterisks from the generated text
    cleaned_text = re.sub(r"\*", "", response.text)
    
    return cleaned_text

# Translate summary to target language
def translate_summary(summary, target_language):
    translator = Translator()
    try:
        translated = translator.translate(summary, dest=target_language)
        return translated.text if translated and hasattr(translated, "text") else "Translation failed."
    except Exception as e:
        return f"Translation failed: {str(e)}"

# Convert text to speech
def text_to_speech(text, language):
    tts = gtts.gTTS(text=text, lang=language)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# Streamlit UI
st.title("YouTube Transcript Summarizer")
youtube_link = st.text_input("Enter YouTube Video Link:")

languages = {
    "Afrikaans": "af",
    "Akan": "ak",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Assamese": "as",
    "Aymara": "ay",
    "Azerbaijani": "az",
    "Bangla": "bn",
    "Basque": "eu",
    "Belarusian": "be",
    "Bhojpuri": "bho",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Burmese": "my",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chinese (Simplified)": "zh-Hans",
    "Chinese (Traditional)": "zh-Hant",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Divehi": "dv",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Ewe": "ee",
    "Filipino": "fil",
    "Finnish": "fi",
    "French": "fr",
    "Galician": "gl",
    "Ganda": "lg",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Guarani": "gn",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "iw",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Kinyarwanda": "rw",
    "Korean": "ko",
    "Krio": "kri",
    "Kurdish": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lingala": "ln",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Māori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Nepali": "ne",
    "Northern Sotho": "nso",
    "Norwegian": "no",
    "Nyanja": "ny",
    "Odia": "or",
    "Oromo": "om",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Quechua": "qu",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Sanskrit": "sa",
    "Scottish Gaelic": "gd",
    "Serbian": "sr",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Southern Sotho": "st",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Thai": "th",
    "Tigrinya": "ti",
    "Tsonga": "ts",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Western Frisian": "fy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu"
}

selected_languages = st.multiselect("Select languages for translation:", list(languages.keys()))

if youtube_link:
    video_id = youtube_link.split("v=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("Get Summarized Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    
    if not transcript_text:
        st.error("Transcript is not available for this video.")
    else:
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
 #Streamlit run app1.py
