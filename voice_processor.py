import os
import tempfile
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import requests
from io import BytesIO
import json
import re
from difflib import SequenceMatcher

class VoiceProcessor:
    def __init__(self, config_path='voice_config.json'):
        self.recognizer = sr.Recognizer()
        self.load_config(config_path)
        
        # Improve recognition settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
    def load_config(self, config_path):
        """Load voice configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # Default configuration if file doesn't exist
            self.config = {
                "voice_commands": {},
                "voice_responses": {},
                "tts_settings": {"language": "en", "slow": False}
            }
        
    def download_audio_from_url(self, audio_url):
        """Download audio file from URL and convert to WAV format"""
        try:
            # Download the audio file
            response = requests.get(audio_url)
            if response.status_code == 200:
                # Convert to AudioSegment
                audio = AudioSegment.from_file(BytesIO(response.content))
                
                # Convert to WAV format for speech recognition
                wav_data = BytesIO()
                audio.export(wav_data, format="wav")
                wav_data.seek(0)
                
                return wav_data
            else:
                raise Exception(f"Failed to download audio: {response.status_code}")
        except Exception as e:
            print(f"Error downloading audio: {str(e)}")
            return None
    
    def speech_to_text(self, audio_data):
        """Convert speech to text using Google Speech Recognition with improved accuracy"""
        try:
            # Create a temporary file for the audio
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data.read())
                temp_file_path = temp_file.name
            
            # Load and process audio file
            with sr.AudioFile(temp_file_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.record(source)
            
            # Try multiple recognition methods for better accuracy
            try:
                # Primary: Google Speech Recognition
                text = self.recognizer.recognize_google(audio, language='en-US')
            except (sr.UnknownValueError, sr.RequestError):
                try:
                    # Fallback: Google with different language model
                    text = self.recognizer.recognize_google(audio, language='en-IN')
                except (sr.UnknownValueError, sr.RequestError):
                    # Final fallback
                    text = self.recognizer.recognize_google(audio)
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            # Process and match commands
            processed_text = self.process_voice_command(text.lower().strip())
            return processed_text
            
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio. Please try again or speak more clearly."
        except sr.RequestError as e:
            return f"Speech recognition service error: {str(e)}"
        except Exception as e:
            return f"Error processing audio: {str(e)}"
    
    def process_voice_command(self, text):
        """Process voice command and match to known commands"""
        # Direct match first
        if text in ['hi', 'hello', 'hey']:
            return text
            
        # Check for command matches
        for command_type, keywords in self.config.get('voice_commands', {}).items():
            for keyword in keywords:
                if self.similarity_match(text, keyword) > 0.8:
                    return keyword
                if keyword in text:
                    return keyword
        
        # Number matching for menu options
        number_words = {
            'one': '1', 'first': '1',
            'two': '2', 'second': '2', 
            'three': '3', 'third': '3',
            'four': '4', 'fourth': '4',
            'five': '5', 'fifth': '5',
            'six': '6', 'sixth': '6',
            'seven': '7', 'seventh': '7'
        }
        
        for word, number in number_words.items():
            if word in text.lower():
                return number
        
        return text
    
    def similarity_match(self, text1, text2):
        """Calculate similarity between two texts"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def text_to_speech(self, text, language='en'):
        """Convert text to speech and return audio data"""
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Save to BytesIO object
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            return audio_buffer
            
        except Exception as e:
            print(f"Error generating speech: {str(e)}")
            return None
    
    def create_voice_response(self, text_response):
        """Create a voice response for the given text"""
        # Clean text for better TTS
        clean_text = self.clean_text_for_tts(text_response)
        return self.text_to_speech(clean_text)
    
    def clean_text_for_tts(self, text):
        """Clean text to make it more suitable for text-to-speech"""
        # Remove emojis and special characters
        import re
        
        # Replace emojis with words
        emoji_replacements = {
            '🎓': 'Education',
            '📚': 'Books',
            '💳': 'Payment',
            '📅': 'Calendar',
            '📞': 'Phone',
            '✅': 'Check',
            '❓': 'Question',
            '🔹': '',
            '•': '',
            '*': '',
            '📧': 'Email',
            '📱': 'Mobile',
            '🏆': 'Trophy',
            '📊': 'Chart',
            '💡': 'Idea',
            '🚀': 'Rocket',
            '🧠': 'Brain',
            '🤔': '',
            '➡️': 'Next',
            '🔄': 'Reload'
        }
        
        for emoji, replacement in emoji_replacements.items():
            text = text.replace(emoji, replacement)
        
        # Remove markdown formatting
        text = re.sub(r'\*([^*]+)\*', r'\1', text)  # Remove *bold*
        text = re.sub(r'_([^_]+)_', r'\1', text)   # Remove _italic_
        
        # Clean up multiple spaces and newlines
        text = re.sub(r'\n+', '. ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()