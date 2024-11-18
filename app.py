from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# URL to your Rasa API
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"  # Adjust the port if necessary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    
    # Send the user's message to Rasa for a response
    response = requests.post(RASA_API_URL, json={"message": user_message})
    
    # Parse the response from Rasa
    bot_reply = response.json()
    
    # Get the bot's response (first message in the list)
    if bot_reply:
        bot_message = bot_reply[0].get("text")
    else:
        bot_message = "Sorry, I couldn't understand that."
    
    return jsonify({'response': bot_message})

if __name__ == '__main__':
    app.run(debug=True)