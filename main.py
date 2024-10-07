from PyPDF2 import PdfReader
from gtts import gTTS
from flask import Flask, request, render_template, flash, redirect, send_from_directory, get_flashed_messages
from werkzeug.utils import secure_filename
import os


username = os.path.dirname(os.path.abspath(__file__)).split('/')[2]
UPLOAD_FOLDER = f'/Users/{username}/Downloads'
AUDIO_FOLDER = f'/Users/{username}/desktop/audio'
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
        file = request.files['file']
        if 'file' not in request.files:
            get_flashed_messages('No file part')
            return redirect(request.url)
        elif file.filename == '':
            flash('No selected file')
            return render_template('upload.html', emptyFile = file.filename)
        elif file.filename.split('.')[-1] != 'pdf' and file.filename != '':
            pdfChecker = file.filename.split('.')[-1]
            return render_template('upload.html', pdfChecker=pdfChecker)  
        elif file and allowed_file(file.filename):
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
            (os.remove(file_path))
            tts.save(audio_path)
            return redirect(f"/uploads/{mp3_filename}")

@app.route('/uploads/<name>')
def download_file(name):
    mp3_file = f"/player/{name}"
    mp3_filename = name[:-4].split("_")
    filename = " ".join(mp3_filename).strip()
    return render_template('mp3.html', mp3_file=mp3_file, name=name, filename=filename)

@app.route('/player/<name>')
def mp3_player(name):
    return send_from_directory(app.config["AUDIO_FOLDER"], name)

@app.route('/upload/<name>/delete', methods=["GET"])
def delete_audio_file(name):
    os.remove(os.path.join(app.config['AUDIO_FOLDER'], name))
    return redirect('/upload')

if __name__ == '__main__':
    app.run(debug=True)