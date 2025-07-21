# Hanyaa Narration TTS Application

1. Project Overview
The Hanyaa Narration application is a web-based Text-to-Speech (TTS) tool built with Python and Streamlit. Its primary purpose is to provide a user-friendly interface for converting written text into high-quality audio narration.
Key Features:
Intuitive Web UI: Built with Streamlit for easy interaction, including text input areas and selection dropdowns.
Dual TTS Engine Support:
Google Cloud TTS: A robust, professional-grade engine providing a wide variety of high-fidelity WaveNet and Standard voices. This is the primary, working engine for the application.
Gemini TTS: An experimental engine intended to use Google's latest generative models. (Note: Currently facing project-level access limitations for the TTS feature).
Multi-language Support: Configured for English, Hindi, and Telugu, with an easily extensible structure.
Real-time Generation: Generates audio on-demand when the user clicks the "Generate Speech" button.
Audio Playback and Download: Allows the user to listen to the generated audio directly in the app and download it as an MP3 file.
