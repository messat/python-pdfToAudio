from PyPDF2 import PdfReader
from gtts import gTTS
from flask import Flask, request, send_file, render_template, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '/Users/muhammadessat/Downloads'
AUDIO_FOLDER = '/Users/muhammadessat/desktop/audio'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
app.secret_key = "super secret key"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route("/uploader", methods=["GET","POST"])
def uploaded_file():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            print(request.url)
            return render_template('error.html')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uploaded_file = file
            file_path = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_file.save(file_path)
            reader = PdfReader(file_path)
            clean_text = ''
            for page_num in range(len(reader.pages)):
                text = reader.pages[page_num].extract_text()
                clean_text += text.strip().replace('\n', ' ')
            tts = gTTS(clean_text, lang='en')
            mp3_filename = filename[:-3] + "mp3"
            audio_path = (os.path.join(app.config['AUDIO_FOLDER'], mp3_filename))
            tts.save(audio_path)
            return redirect(url_for('upload_file', name=mp3_filename))
        return "file uploaded successfully"

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["AUDIO_FOLDER"], name)


if __name__ == '__main__':
    app.run(debug=True)