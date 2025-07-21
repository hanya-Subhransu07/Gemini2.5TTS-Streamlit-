import streamlit as st
import google.generativeai as genai
import io
import base64
from PIL import Image

# --- Page Configuration ---
st.set_page_config(
    page_title="Hanyaa Narration",
    layout="centered",
    page_icon="🎙️"
)

# --- Custom CSS Styling ---
# (Your CSS remains the same)
st.markdown("""
    <style>
        body {
            background-color: #0d1b2a;
            font-family: 'Segoe UI', sans-serif;
        }
        .main .block-container {
            padding-top: 3rem;
            padding-bottom: 3rem;
        }
        
        /* Logo styling */
        .logo-container {
            position: fixed;
            top: 10px;
            right: 20px;
            z-index: 1000;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 10px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .logo-container img {
            width: 120px;
            height: auto;
            border-radius: 8px;
        }
        
        h1 {
            text-align: center;
            color: #ffffff;
            font-weight: 700;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 5px rgba(0,0,0,0.3);
        }
        .stSelectbox > div, .stTextArea textarea {
            background-color: #1c1c1e;
            color: #ffffff;
            border: 1px solid #3a3a3c;
            border-radius: 8px;
        }
        .stSlider > div {
            background-color: transparent;
        }
        .stButton > button {
            background-color: #1e747c;
            color: white;
            font-weight: bold;
            font-size: 1.1rem;
            padding: 0.75rem 1.5rem;
            border-radius: 10px;
            border: none;
            width: 100%;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .stButton > button:hover {
            background-color: #145c5e;
            transition: 0.3s;
        }
        .stDownloadButton > button {
            background-color: #1c7c54;
            color: white;
        }
        .stDownloadButton > button:hover {
            background-color: #146c45;
        }
        
        /* Error styling */
        .error-message {
            background-color: #2d1b1b;
            color: #ff6b6b;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #ff6b6b;
            margin: 10px 0;
        }
        
        /* Success styling */
        .success-message {
            background-color: #1b2d1b;
            color: #51cf66;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #51cf66;
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

def add_logo():
    logo_path = "Normal.png"
    try:
        logo = Image.open(logo_path)
        st.markdown(
            """
            <style>
                .logo-left {
                    position: fixed;
                    top: 10px;
                    left: 15px;
                    z-index: 100;
                    background-color: rgba(255, 255, 255, 0.05);
                    padding: 5px 10px;
                    border-radius: 8px;
                }
                .logo-left img {
                    height: 100px;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown(f'<div class="logo-left"><img src="data:image/png;base64,{get_base64(logo_path)}" alt="logo"></div>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Logo file 'Normal.png' not found.")


def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


# --- Initialize Gemini ---
@st.cache_resource
def init_gemini():
    try:
        # Configure the Gemini API key from Streamlit secrets
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        return True
    except Exception as e:
        st.error(f"Failed to initialize Gemini: {e}")
        return False

# --- Gemini TTS Function ---
import google.generativeai as genai
import google.ai.generativelanguage as glm # Import the low-level types

def synthesize_text_gemini(text, voice_style="default"):
    """
    Synthesize text using a modern Gemini model (Pro or Flash) by specifying
    the audio mime type in the generation config. This is the correct method.
    """
    try:
        # We use a powerful text model and instruct it to output audio.
        # gemini-1.5-pro is a great choice. gemini-1.5-flash should also work.
        model = genai.GenerativeModel('gemini-1.5-pro')

        # The key is to provide the text directly as the content and use
        # generation_config to specify the desired output format (MIME type).
        response = model.generate_content(
            text, # The text to be synthesized is the main content
            generation_config=glm.GenerationConfig(
                response_mime_type="audio/mpeg" # Request MP3 audio output
            )
        )

        # When the request is correct, the response will contain a Part with a blob.
        if response.parts and response.parts[0].blob:
            # The audio data is in the 'data' attribute of the 'blob'
            return response.parts[0].blob.data, None
        else:
            # This handles cases where the model might refuse the request
            error_info = "The model did not return audio. Check the prompt feedback."
            try:
                error_info += f" Safety Ratings: {response.prompt_feedback}"
            except Exception:
                pass
            return None, f"Gemini TTS Error: {error_info}"

    except Exception as e:
        error_message = f"Gemini TTS Error: {str(e)}"
        if "API_KEY_INVALID" in str(e):
            error_message += " Please check if your GOOGLE_API_KEY is configured correctly."
        elif "PERMISSION_DENIED" in str(e) or "access" in str(e).lower():
            error_message += " Your API key may not have permission for the selected model. Check your Google Cloud project."
        # This is a new, important error to catch!
        elif "response_mime_type" in str(e):
             error_message += " The selected model may not support audio output. Try 'gemini-1.5-pro'."
        return None, error_message
# --- Fallback Google TTS Function ---
def synthesize_text_google(text, voice, speed, pitch):
    """
    Fallback Google TTS implementation
    """
    try:
        from google.cloud import texttospeech
        
        client = texttospeech.TextToSpeechClient()

        input_text = texttospeech.SynthesisInput(text=text)
        voice_params = texttospeech.VoiceSelectionParams(
            language_code="-".join(voice.split("-")[:2]),
            name=voice
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speed,
            pitch=pitch
        )

        response = client.synthesize_speech(
            request={"input": input_text, "voice": voice_params, "audio_config": audio_config}
        )

        return response.audio_content, None
    except Exception as e:
        return None, str(e)

# --- Main Application ---
def main():
    add_logo()
    
    st.markdown("<h1> Narration Generation</h1>", unsafe_allow_html=True)
    
    # Initialize Gemini
    if not init_gemini():
        st.stop()
    
    engine = st.selectbox(
        "TTS Engine", 
        options=["Gemini TTS", "Google Cloud TTS"], 
        index=0
    )
    
    lang_map = {
        "English": "en-US",
        "Hindi": "hi-IN",
        "Telugu": "te-IN",
    }
    
    language = st.selectbox("Language", options=list(lang_map.keys()), index=0)
    
    if engine == "Gemini TTS":
    # The gemini-1.5-flash model uses a standard high-quality voice.
    # A specific "voice style" parameter is not directly available in this API format.
    # We will create a placeholder variable.
        voice = "default" 
        st.info("The Gemini 1.5 Flash model will be used with its standard, high-quality voice.")
    else:
        voices = {
            "en-US": ["en-US-Wavenet-D", "en-US-Wavenet-F", "en-US-Standard-C"],
            "hi-IN": ["hi-IN-Wavenet-A", "hi-IN-Standard-A"],
            "te-IN": ["te-IN-Wavenet-A"],
        }
        voice = st.selectbox("Speaker", options=voices.get(lang_map[language], []))
    
    st.markdown("### Text Input")
    text_input = st.text_area("Enter Text", height=150, placeholder="Enter the text you want to convert to speech...")
    
    generate = st.button("🔊 Generate Speech")
    
    if generate:
        if not text_input:
            st.markdown('<div class="error-message">⚠️ Please enter some text to convert.</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Generating speech..."):
                if engine == "Gemini TTS":
                    audio, error = synthesize_text_gemini(text_input, voice)
                else:
                    # Note: You will need to handle authentication for Google Cloud TTS separately
                    # if you haven't set up Application Default Credentials.
                    audio, error = synthesize_text_google(text_input, voice, 1.0, 0.0)
                
                if error:
                    st.markdown(f'<div class="error-message">❌ Error: {error}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="success-message">✅ Speech generated successfully!</div>', unsafe_allow_html=True)
                    st.audio(audio, format="audio/mpeg")
                    st.download_button(
                        "📥 Download Audio", 
                        data=audio, 
                        file_name=f"tts_output_{engine.lower().replace(' ', '_')}.mp3", 
                        mime="audio/mpeg"
                    )
    
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #888; margin-top: 2rem;">Powered by HANYAA - Together, We\'ll Create Magic ✨</div>', 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
    
    
    
# import streamlit as st
# import google.generativeai as genai
# import io
# import base64
# from PIL import Image
# import requests
# from io import BytesIO

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="Hanyaa Naration",
#     layout="centered",
#     page_icon="🎙️"
# )

# # --- Custom CSS Styling ---
# st.markdown("""
#     <style>
#         body {
#             background-color: #0d1b2a;
#             font-family: 'Segoe UI', sans-serif;
#         }
#         .main .block-container {
#             padding-top: 3rem;
#             padding-bottom: 3rem;
#         }
        
#         /* Logo styling */
#         .logo-container {
#             position: fixed;
#             top: 10px;
#             right: 20px;
#             z-index: 1000;
#             background-color: rgba(255, 255, 255, 0.1);
#             border-radius: 10px;
#             padding: 10px;
#             backdrop-filter: blur(10px);
#             border: 1px solid rgba(255, 255, 255, 0.2);
#         }
        
#         .logo-container img {
#             width: 120px;
#             height: auto;
#             border-radius: 8px;
#         }
        
#         h1 {
#             text-align: center;
#             color: #ffffff;
#             font-weight: 700;
#             margin-bottom: 2rem;
#             text-shadow: 1px 1px 5px rgba(0,0,0,0.3);
#         }
#         .stSelectbox > div, .stTextArea textarea {
#             background-color: #1c1c1e;
#             color: #ffffff;
#             border: 1px solid #3a3a3c;
#             border-radius: 8px;
#         }
#         .stSlider > div {
#             background-color: transparent;
#         }
#         .stButton > button {
#             background-color: #1e747c;
#             color: white;
#             font-weight: bold;
#             font-size: 1.1rem;
#             padding: 0.75rem 1.5rem;
#             border-radius: 10px;
#             border: none;
#             width: 100%;
#             box-shadow: 0 5px 15px rgba(0,0,0,0.2);
#         }
#         .stButton > button:hover {
#             background-color: #145c5e;
#             transition: 0.3s;
#         }
#         .stDownloadButton > button {
#             background-color: #1c7c54;
#             color: white;
#         }
#         .stDownloadButton > button:hover {
#             background-color: #146c45;
#         }
        
#         /* Error styling */
#         .error-message {
#             background-color: #2d1b1b;
#             color: #ff6b6b;
#             padding: 15px;
#             border-radius: 8px;
#             border-left: 4px solid #ff6b6b;
#             margin: 10px 0;
#         }
        
#         /* Success styling */
#         .success-message {
#             background-color: #1b2d1b;
#             color: #51cf66;
#             padding: 15px;
#             border-radius: 8px;
#             border-left: 4px solid #51cf66;
#             margin: 10px 0;
#         }
#     </style>
# """, unsafe_allow_html=True)

# from PIL import Image

# def add_logo():
#     logo_path = "Normal.png"  # or replace with the second uploaded file name if needed
#     logo = Image.open(logo_path)
#     st.markdown(
#         """
#         <style>
#             .logo-left {
#                 position: fixed;
#                 top: 10px;
#                 left: 15px;
#                 z-index: 100;
#                 background-color: rgba(255, 255, 255, 0.05);
#                 padding: 5px 10px;
#                 border-radius: 8px;
#             }
#             .logo-left img {
#                 height: 100px;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )
#     st.markdown(f'<div class="logo-left"><img src="data:image/png;base64,{get_base64(logo_path)}" alt="logo"></div>', unsafe_allow_html=True)

# def get_base64(file_path):
#     with open(file_path, "rb") as f:
#         data = f.read()
#     return base64.b64encode(data).decode()


# # --- Initialize Gemini ---
# @st.cache_resource
# def init_gemini():
#     try:
#         # Configure the Gemini API key from Streamlit secrets
#         genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
#         return True
#     except Exception as e:
#         st.error(f"Failed to initialize Gemini: {e}")
#         return False

# # --- Gemini TTS Function ---
# @st.cache_data
# def synthesize_text_gemini(text, voice_style="puck"):
#     """
#     Synthesize text using Gemini's Text-to-Speech capabilities.
#     """
#     try:
#         # Select the TTS model. [2, 5]
#         model = genai.GenerativeModel('gemini-2.5-flash-preview-tts')

#         # The prompt for TTS is a direct instruction to read the text. [5, 19]
#         prompt = f"Read this text: {text}"

#         # Generate the audio content.
#         # The response modality needs to be set to "audio". [1, 19]
#         response = model.generate_content(
#             prompt,
#             generation_config=genai.types.GenerationConfig(
#                 response_modality=genai.types.GenerateContentResponse.AUDIO,
#                 speech=genai.types.SpeechConfig(
#                     voice=genai.types.VoiceConfig(
#                         voice=voice_style
#                     )
#                 )
#             )
#         )

#         # The audio data is in the first part of the response.
#         return response.parts[0].audio, None

#     except Exception as e:
#         return None, f"Gemini TTS Error: {str(e)}"
    
    

# # --- Fallback Google TTS Function ---
# def synthesize_text_google(text, voice, speed, pitch):
#     """
#     Fallback Google TTS implementation
#     """
#     try:
#         from google.cloud import texttospeech
        
#         client = texttospeech.TextToSpeechClient()

#         input_text = texttospeech.SynthesisInput(text=text)
#         voice_params = texttospeech.VoiceSelectionParams(
#             language_code="-".join(voice.split("-")[:2]),
#             name=voice
#         )
#         audio_config = texttospeech.AudioConfig(
#             audio_encoding=texttospeech.AudioEncoding.MP3,
#             speaking_rate=speed,
#             pitch=pitch
#         )

#         response = client.synthesize_speech(
#             request={"input": input_text, "voice": voice_params, "audio_config": audio_config}
#         )

#         return response.audio_content, None
#     except Exception as e:
#         return None, str(e)

# # --- Main Application ---
# def main():
#     # Add logo
#     add_logo()
    
#     # Main title
#     st.markdown("<h1> Narration Generation</h1>", unsafe_allow_html=True)
    
#     # Configuration section
#     # st.markdown("### Configuration")
    
#     # TTS Engine selection
#     engine = st.selectbox(
#         "TTS Engine", 
#         options=["Gemini 2.5 Flash", "Google Cloud TTS"], 
#         index=0
#     )
    
#     # Language selection
#     lang_map = {
#         "English": "en-US",
#         "Hindi": "hi-IN",
#         "Telugu": "te-IN",
#     }
    
#     language = st.selectbox("Language", options=list(lang_map.keys()), index=0)
    
#     # Voice selection (different for each engine)
#     if engine == "Gemini 2.5 Flash":
#         voice_options = ["Natural", "Expressive", "Calm", "Energetic"]
#         voice = st.selectbox("Voice Style", options=voice_options)
#     else:
#         voices = {
#             "en-US": ["en-US-Wavenet-D", "en-US-Wavenet-F", "en-US-Standard-C"],
#             "hi-IN": ["hi-IN-Wavenet-A", "hi-IN-Standard-A"],
#             "te-IN": ["te-IN-Wavenet-A"],
#         }
#         voice = st.selectbox("Speaker", options=voices.get(lang_map[language], []))
    
#     # Text input
#     st.markdown("### Text Input")
#     text_input = st.text_area("Enter Text", height=150, placeholder="Enter the text you want to convert to speech...")
    
#     # Audio settings
#     st.markdown("### Audio Settings")
#     col1, col2 = st.columns(2)
#     with col1:
#         speed = st.slider("Speed", min_value=0.25, max_value=4.0, value=1.0, step=0.1)
#     with col2:
#         pitch = st.slider("Pitch", min_value=-20.0, max_value=20.0, value=0.0, step=1.0)
    
#     # Generate button
#     generate = st.button("🔊 Generate Speech")
    
#     # Processing
#     if generate:
#         if not text_input:
#             st.markdown('<div class="error-message">⚠️ Please enter some text to convert.</div>', unsafe_allow_html=True)
#         else:
#             with st.spinner("Generating speech..."):
#                 if engine == "Gemini 2.5 Flash":
#                     audio, error = synthesize_text_gemini(text_input, voice.lower(), speed, pitch)
#                 else:
#                     audio, error = synthesize_text_google(text_input, voice, speed, pitch)
                
#                 if error:
#                     st.markdown(f'<div class="error-message">❌ Error: {error}</div>', unsafe_allow_html=True)
                    
#                     # Show setup instructions for Gemini
#                     if "Gemini" in error:
#                         st.markdown("""
#                         ### Setup Instructions for Gemini TTS:
#                         1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
#                         2. Set your API key in the code: `genai.configure(api_key="YOUR_API_KEY")`
#                         3. Update the `synthesize_text_gemini` function based on the actual Gemini TTS API documentation
#                         4. Install required packages: `pip install google-generativeai`
#                         """)
#                 else:
#                     st.markdown('<div class="success-message">✅ Speech generated successfully!</div>', unsafe_allow_html=True)
#                     st.audio(audio, format="audio/mp3")
#                     st.download_button(
#                         "📥 Download Audio", 
#                         data=audio, 
#                         file_name=f"tts_output_{engine.lower().replace(' ', '_')}.mp3", 
#                         mime="audio/mpeg"
#                     )
    
#     # Footer
#     st.markdown("---")
#     st.markdown(
#         '<div style="text-align: center; color: #888; margin-top: 2rem;">Powered by HANYAA - Together, We\'ll Create Magic ✨</div>', 
#         unsafe_allow_html=True
#     )

# if __name__ == "__main__":
#     main()