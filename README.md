# Gemini2.5TTS-Streamlit- Hanyaa Narration 🎙️

A modern, AI-powered text-to-speech application built with Streamlit and Google's Gemini AI, featuring a sleek dark theme interface and multiple TTS engine options.

## Features ✨

- **Multiple TTS Engines**: Choose between Gemini TTS and Google Cloud TTS
- **Multi-language Support**: English, Hindi, and Telugu
- **Modern Dark UI**: Elegant dark theme with glassmorphism effects
- **Voice Customization**: Different voice styles and speakers
- **Audio Controls**: Adjustable speed and pitch settings (for Google Cloud TTS)
- **Download Support**: Save generated audio as MP3 files
- **Real-time Processing**: Generate speech with live feedback


## Demo 🎥

### Working Video
Check out the demo video to see Hanyaa Narration in action:

![Demo Video](https://github.com/hanya-Subhransu07/Gemini2.5TTS-Streamlit-/blob/main/Geimini2.5%20TTS%20Integration.mp4)

*Can't see the video? [Click here to download](https://github.com/hanya-Subhransu07/Gemini2.5TTS-Streamlit-/blob/main/Geimini2.5%20TTS%20Integration.mp4)*
## Screenshots

The application features a beautiful dark interface with:
- Fixed logo positioning
- Gradient backgrounds with blur effects
- Modern form controls
- Success/error message styling
- Responsive design

## Installation

### Prerequisites

- Python 3.7+
- Google API key for Gemini
- (Optional) Google Cloud credentials for Google Cloud TTS

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Gemini2.5TTS-Streamlit-
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit google-generativeai pillow google-cloud-texttospeech
   ```

3. **Add your logo**
   - Place your logo file as `Normal.png` in the project root directory

4. **Configure API keys**
   
   **Method 1: Using Streamlit Secrets (Recommended for deployment)**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   GOOGLE_API_KEY = "your_gemini_api_key_here"
   ```

   **Method 2: Environment Variables**
   ```bash
   export GOOGLE_API_KEY="your_gemini_api_key_here"
   ```

### Getting API Keys

#### Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your configuration

#### Google Cloud TTS (Optional)
1. Create a Google Cloud Project
2. Enable the Text-to-Speech API
3. Create service account credentials
4. Set up authentication (see Google Cloud documentation)

## Usage

### Running the Application

```bash
streamlit run app_streamlit.py
```

The application will be available at `http://localhost:8501`

### Using the Interface

1. **Select TTS Engine**: Choose between "Gemini TTS" or "Google Cloud TTS"
2. **Choose Language**: Select from English, Hindi, or Telugu
3. **Pick Voice**: 
   - Gemini TTS: Uses default high-quality voice
   - Google Cloud TTS: Choose from available voice models
4. **Enter Text**: Input the text you want to convert to speech
5. **Generate**: Click the "🔊 Generate Speech" button
6. **Listen & Download**: Play the audio and optionally download it

## Configuration Options

### TTS Engines

#### Gemini TTS
- Uses `gemini-2.5-preview-TTS` model
- Outputs high-quality MP3 audio
- Standard voice with natural intonation
- Faster processing times

#### Google Cloud TTS
- Multiple voice options per language
- Adjustable speed and pitch controls
- WaveNet and Standard voice types
- Requires additional authentication setup

### Supported Languages & Voices

| Language | Code | Available Voices (Google Cloud) |
|----------|------|--------------------------------|
| English | en-US | Wavenet-D, Wavenet-F, Standard-C |
| Hindi | hi-IN | Wavenet-A, Standard-A |
| Telugu | te-IN | Wavenet-A |

## File Structure

```
hanyaa-narration/
├── app_streamlit.py          # Main application file
├── Normal.png                # Logo file
├── .streamlit/
│   └── secrets.toml         # API keys (create this)
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## Dependencies

- `streamlit`: Web application framework
- `google-generativeai`: Gemini AI integration
- `pillow`: Image processing for logo
- `google-cloud-texttospeech`: Google Cloud TTS (optional)

## Error Handling

The application includes comprehensive error handling for:
- Missing API keys
- Invalid model permissions
- Network connectivity issues
- Unsupported audio formats
- Missing logo files

## Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add your secrets in the Streamlit Cloud dashboard:
   - `GOOGLE_API_KEY`: Your Gemini API key
4. Deploy the application

### Local Deployment

For production deployment, consider:
- Using environment variables for API keys
- Setting up proper logging
- Configuring HTTPS
- Adding rate limiting

## Troubleshooting

### Common Issues

1. **"Failed to initialize Gemini" Error**
   - Check if your API key is correctly set
   - Verify the key has proper permissions

2. **"Logo file not found" Warning**
   - Ensure `Normal.png` exists in the project root
   - Check file permissions

3. **Google Cloud TTS Authentication Errors**
   - Set up Application Default Credentials
   - Check service account permissions

4. **Audio Generation Fails**
   - Verify your API quota hasn't been exceeded
   - Check network connectivity
   - Ensure the selected model supports audio output

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **HANYAA Team** - "Together, We'll Create Magic ✨"
- **Google AI** - For Gemini and Cloud TTS services
- **Streamlit** - For the amazing web framework

## Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section above
- Review Google AI Studio documentation for API-related questions

---

**Powered by HANYAA - Together, We'll Create Magic ✨**
