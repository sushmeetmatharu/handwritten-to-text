import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from ocr_engine import extract_text_from_image

app = Flask(__name__)

# Configure file upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Check if the uploaded file is an allowed image type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = ""
    uploaded_image_path = None

    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part in the request"
        
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Extract text from the uploaded image
            extracted_text = extract_text_from_image(file_path)
            uploaded_image_path = file_path  # Store the uploaded image path

    return render_template('index.html', extracted_text=extracted_text, uploaded_image_path=uploaded_image_path)

if __name__ == '__main__':
    app.run(debug=True)
