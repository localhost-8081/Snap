import os
from PIL import Image as PILImage
from flask import Flask, render_template, request

import google.generativeai as genai

# Configure the generative AI model
API_KEY = "AIzaSyArF2Fp_p07sadEH0x12nnM5frc6kEPdZo"
genai.configure(api_key=API_KEY)

# Function to load OpenAI model and get responses
def get_gemini_response(input_text, image_path):
    model = genai.GenerativeModel('gemini-pro-vision')
    image = PILImage.open(image_path)
    if input_text != "":
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content(image)
    return response.text

app = Flask(__name__)

# Create the uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    input_text = request.form['input_text']
    image = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)
    response = get_gemini_response(input_text, image_path)
    os.remove(image_path)
    return response

if __name__ == "__main__":
    app.run(debug=True)
