from PyPDF2 import PdfReader
from gtts import gTTS
from flask import Flask, request, render_template, flash, redirect, send_from_directory, send_file
from werkzeug.utils import secure_filename
import os
import time
import speech_recognition as sr
from pydub import AudioSegment
from languages.languageSelect import all_languages
from languages.accent import accents_tld
app = Flask(__name__)



username = os.path.dirname(os.path.abspath(__file__)).split('/')[2]

UPLOAD_FOLDER = 'uploads'
AUDIO_FOLDER = 'audio'

ALLOWED_EXTENSIONS = {'pdf'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['AUDIO_FOLDER']):
    os.makedirs(app.config['AUDIO_FOLDER'])

app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000
app.secret_key = "super secret key"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/upload')
def upload_file():
    return render_template('upload.html', all_languages=all_languages, accents_tld=accents_tld)


@app.route("/uploader", methods=["GET","POST"])
def uploaded_file():
    if request.method == "POST":
        language_spoken = request.form.get('language')
        accent = request.form.get('accent')
        file = request.files['file']
        if 'file' not in request.files:
            flash('No file part')
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
            file_length = os.stat(file_path).st_size
            if file_length <= app.config['MAX_CONTENT_LENGTH']:
                reader = PdfReader(file_path)
                clean_text = ''
                for page_num in range(len(reader.pages)):
                    text = reader.pages[page_num].extract_text()
                    clean_text += text.strip().replace('\n', ' ')
                # time.sleep(3)
                tts = gTTS(clean_text, lang=str(language_spoken), tld=str(accent))
                mp3_filename = filename[:-3] + "mp3"
                audio_path = (os.path.join(app.config['AUDIO_FOLDER'], mp3_filename))
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

@app.route('/upload/<name>/download', methods=["GET"])
def download_audio_file(name):
    uploads = os.path.join(app.config['AUDIO_FOLDER'], name)
    return send_file(uploads, as_attachment=True)

@app.route('/upload/<name>/view', methods=["GET"])
def view_transcript(name):
    mp3_path = os.path.join(app.config['AUDIO_FOLDER'], name)
    wav_path = os.path.join(app.config['AUDIO_FOLDER'], name[0:-4] + '.wav')
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format='wav')
    file_audio = sr.AudioFile(wav_path)

    r = sr.Recognizer()

    segment_duration = 5 * 60 
    full_transcript = ""
    with file_audio as source:
        duration = int(sound.duration_seconds)
        for start in range(0, duration, segment_duration):
            audio_text = r.record(source, duration=segment_duration)
            try:
                full_transcript += r.recognize_google(audio_text) + " "
            except sr.RequestError as e:
                print(f"API request error: {e}")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio")
    
        file_name_text = name[0:-4]
    return render_template('transcript.html', full_transcript=full_transcript, file_name_text=file_name_text)




if __name__ == '__main__':
    app.run(debug=True)