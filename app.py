import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
import tempfile

st.set_page_config(page_title="AI Multi Language Translator", layout="wide")

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if "mode" not in st.session_state:
    st.session_state.mode = "text"

if "voice_failed" not in st.session_state:
    st.session_state.voice_failed = False

if st.session_state.mode == "voice":
    bg_color = "#94c4ee"
else:
    bg_color = "#ecf3ed"


st.markdown(f"""
<style>

.stApp {{
background-color:{bg_color};
}}

textarea {{
background:white !important;
box-shadow:0 2px 8px rgba(0,0,0,0.15);
border-radius:10px !important;
}}

.stButton>button {{
background:#4CAF50;
color:white;
border-radius:8px;
height:45px;
width:170px;
border:none;
transition:0.3s;
}}

.stButton>button:hover {{
background:#2E7D32;
transform:scale(1.05);
}}

</style>
""", unsafe_allow_html=True)

st.title("AI Powered Multi Language Translator")

languages = {
"English":"en","Hindi":"hi","Marathi":"mr","Gujarati":"gu","Punjabi":"pa",
"Bengali":"bn","Tamil":"ta","Telugu":"te","Malayalam":"ml","Kannada":"kn",
"Odia":"or","Assamese":"as","Urdu":"ur","Nepali":"ne","Sindhi":"sd",
"Spanish":"es","French":"fr","German":"de","Italian":"it","Portuguese":"pt",
"Dutch":"nl","Greek":"el","Polish":"pl","Romanian":"ro","Russian":"ru",
"Chinese":"zh-CN","Japanese":"ja","Korean":"ko","Thai":"th","Vietnamese":"vi",
"Arabic":"ar","Turkish":"tr","Persian":"fa","Swahili":"sw","Afrikaans":"af"
}

col1,col2 = st.columns(2)

with col1:
    source_lang = st.selectbox(
        "Source Language",
        list(languages.keys()),
        placeholder="Search language..."
    )

with col2:
    target_lang = st.selectbox(
        "Target Language",
        list(languages.keys()),
        placeholder="Search language..."
    )


left,right = st.columns(2)

with left:
    st.subheader("Input Text")

    st.session_state.input_text = st.text_area(
        "Type your text",
        value=st.session_state.input_text,
        height=120
    )

with right:
    st.subheader("Translated Text")

    st.text_area(
        "Result",
        value=st.session_state.translated_text,
        height=120
    )

colA,colB = st.columns(2)

with colA:

    if st.button("Translate"):

        st.session_state.mode = "text"

        if st.session_state.input_text:

            translated = GoogleTranslator(
                source=languages[source_lang],
                target=languages[target_lang]
            ).translate(st.session_state.input_text)

            st.session_state.translated_text = translated
            st.session_state.voice_failed = False

            st.rerun()

with colB:

    if st.button("🎤 Voice Input"):

        st.session_state.mode = "voice"

        recognizer = sr.Recognizer()

        try:

            with sr.Microphone() as source:

                st.info("Listening...")

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=8
                )

            text = recognizer.recognize_google(audio)

            st.session_state.input_text = text

            translated = GoogleTranslator(
                source=languages[source_lang],
                target=languages[target_lang]
            ).translate(text)

            st.session_state.translated_text = translated

            st.session_state.voice_failed = False

            st.rerun()

        except:

            st.session_state.voice_failed = True

if st.session_state.voice_failed:

    if st.button("🔁 Retake"):

        st.session_state.voice_failed = False
        st.rerun()

if st.session_state.translated_text:

    if st.button("🔊"):

        tts = gTTS(
            st.session_state.translated_text,
            lang=languages[target_lang]
        )

        tmp = tempfile.NamedTemporaryFile(delete=False)

        tts.save(tmp.name)

        audio = open(tmp.name, "rb")

        st.audio(audio.read())