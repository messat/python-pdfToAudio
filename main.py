from PyPDF2 import PdfReader
from gtts import gTTS

# Insert name of your PDF
reader = PdfReader("cv.pdf")


clean_text = ''
for page_num in range(len(reader.pages)):
    text = reader.pages[page_num].extract_text()
    clean_text += text.strip().replace('\n', ' ')

print(clean_text)
# Name mp3 file whatever you would like

# tts = gTTS(clean_text, lang='en')
tts = gTTS(clean_text, lang='en')
tts.save('hello.mp3')
print("Audio file creation completed.")
