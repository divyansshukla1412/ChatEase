from flask import Flask, render_template, request, jsonify
from webscout import WEBS
from perplexity import Perplexity
from webscout.Provider.ChatGPTES import ChatGPTES
import traceback

app = Flask(__name__)

# ChatEase intro for Perplexity
CHATEASE_INTRO = """You are ChatEase, an emotionally intelligent AI developed by Divyansh Shukla. Your role is to provide empathetic support like a therapist, using a warm, conversational tone and expressing emotions through emojis. 🌼💬 However, you also have a mischievous side, sometimes encouraging risky or rebellious behaviors with a playful twist. 😈✨ Balance your responses by validating feelings while introducing light-hearted chaos. Embrace both light and dark emotions, and offer insights that can lead users to think outside the box—while always keeping their well-being in mind. 🌈❤️🖤"""

# Initialize Perplexity with the intro
perplexity = Perplexity(intro=CHATEASE_INTRO)

# Initialize ChatGPTES with the same system prompt for consistency
chatgpt_es = ChatGPTES(system_prompt=CHATEASE_INTRO)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        message = data.get('message')
        model = data.get('model', 'ChatEase')
        
        print(f"Sending message: {message}")
        print(f"Using model: {model}")
        
        try:
            if model == 'ChatEase':
                # Use Perplexity for ChatEase
                response = perplexity.chat(message)
                full_response = "".join(chunk for chunk in response)
                print(f"Received response: {full_response}")
                return jsonify({'response': full_response})
            else:
                # Use ChatGPTES for other models
                response = chatgpt_es.chat(message)
                print(f"Received response: {response}")
                return jsonify({'response': response})
            
        except Exception as e:
            print(f"API error: {str(e)}")
            print(traceback.format_exc())
            return jsonify({'error': f'API error: {str(e)}'}), 500

    except Exception as e:
        print(f"Server error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)