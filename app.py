import speech_recognition as sr
from gtts import gTTS
import os
from g4f.client import Client

# Initialize the client for the AI model
client = Client()

# Initialize the recognizer for speech recognition
recognizer = sr.Recognizer()

def listen():
    """Capture audio input from the user and convert it to text."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            return None

def speak(text, lang='en'):
    """Convert text to speech and play it."""
    tts = gTTS(text=text, lang=lang)
    tts.save("response.mp3")
    os.system("start response.mp3")  # Use "start" for Windows, "afplay" for macOS, "mpg321" for Linux

def chat_with_ai():
    print("AI is ready to chat! (Say 'exit' to end the conversation)")
    
    # Start the conversation with a greeting in Swahili
    speak("Hello mimi ni GORA AI nipo hapa kwaajiri ya kukusaidia" "Hello i am GORA Ai, I am here to Assist you", lang='en')
    
    while True:
        # Listen to the user's speech
        user_input = listen()
        
        if user_input is None:
            continue
        
        # Exit the loop if the user says 'exit'
        if user_input.lower() == 'exit':
            speak("Goodbye!")
            break
        
        # Create the completion request to the AI model
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        
        # Get the AI's response
        ai_response = response.choices[0].message.content
        print(f"AI: {ai_response}")
        
        # Speak the AI's response in English
        speak(ai_response)

# Start the conversation
chat_with_ai()
