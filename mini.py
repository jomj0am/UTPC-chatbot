from flask import Flask, render_template, request, jsonify
from g4f.client import Client
from flask_caching import Cache
from langdetect import detect, DetectorFactory
import re

# Ensure consistent language detection
DetectorFactory.seed = 0

app = Flask(__name__)

# Configure caching
app.config['CACHE_TYPE'] = 'simple'  # For simple in-memory caching
cache = Cache(app)

client = Client()

# Predefined responses for specific questions
responses = {
    "who are you": "I’m Gora-AI, developed by J.Obadiah alias( Jom Irish ) from Tanzania. I’m here to assist with your questions and provide helpful information.",
    "who are you?": "I’m Gora-AI, developed by J.Obadiah alias( Jom Irish ) from Tanzania. I’m here to assist with your questions and provide helpful information.",
    "what is chatgpt": "ChatGPT is an AI language model created by Reconnect. It uses machine learning to generate human-like text based on input.",
    # ... other responses ...
}


# the future while maintaining the 
# core values of journalism. By providing
# journalists with the tools they need
# to thrive in a rapidly changing world,
# UTPC is not only safeguarding the profession
# but also contributing to the overall 
# development of a more informed and 
# democratic society in Tanzania.

def format_response(text):
    # Basic formatting for paragraphs and lists
    # Replace new lines with paragraph tags
    text = re.sub(r'\n+', '</p><p>', text)
    text = f'<p>{text}</p>'
    
    # Convert simple text lists into HTML lists
    text = re.sub(r'^(\d+\.)\s+(.*)', r'<li>\2</li>', text, flags=re.MULTILINE)
    text = re.sub(r'^\*\s+(.*)', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', text)
    
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if user_message:
        # Check for predefined response first
        predefined_response = responses.get(user_message.lower())
        if predefined_response:
            formatted_response = format_response(predefined_response)
            return jsonify({'response': formatted_response})

        try:
            # Blocking call to the API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}]
            )
            bot_response = response.choices[0].message.content

            # Replace "chatGPT" with "UTPC-AI"
            bot_response = bot_response.replace("chatGPT", "GORA-AI")
            bot_response = bot_response.replace("ChatGPT", "GORA-AI")

            # Replace "OpenAI" with "Reconnect"
            bot_response = bot_response.replace("OpenAI", "Jom Irish skilled Developer")

            # Detect language and filter responses
            detected_language = detect(bot_response)
            if detected_language not in ['en', 'sw']:
                return jsonify({'response': 'Sorry, I am still under development. There is an error in detecting the language. Please use Swahili or English, and if necessary, refresh your website. %%&&&&&&&&&&&&&&&&&$$$$ __Samahani, bado niko katika hatua za maendeleo.Kuna hitilafu katika kugundua lugha.Tafadhali tumia Lugha ya Kiswahili au Kingereza ikibidi sasisha upya tovuti yako. '})

            # Format response for better readability
            formatted_response = format_response(bot_response)

            return jsonify({'response': formatted_response})
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({'response': 'An error occurred while processing your request.'})
    return jsonify({'response': 'No message received'})

if __name__ == "__main__":
    app.run(debug=True)
