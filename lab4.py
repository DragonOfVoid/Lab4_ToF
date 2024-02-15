import json, os
from io import BytesIO
from PIL import Image
import pyttsx3, vosk, pyaudio, requests

tts = pyttsx3.init()

voices = tts.getProperty('voices')
tts.setProperty('voices', 'en')

for voice in voices:
    #print(voice.name)
    if voice.name == 'Microsoft David Desktop - English (United States)':
        tts.setProperty('voice', voice.id)
model = vosk.Model('model_small')
record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 input=True,
                 frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']
def speak(say):
    tts.say(say)
    tts.runAndWait()

print('start')
url = ''
for text in listen():
    print("recived: {}".format(text))
    if text == 'close':
        quit()
    elif text == 'next':
        req =requests.get('https://dog.ceo/api/breeds/image/random')
        data = req.json()
        url = data['message']
        print(url)
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
    elif text =='show':
        if url:
            img.show('image')
        else:
            speak('nothing to show')
    elif text == 'save':
        if url:
            img.save('image.jpg')
            speak('recorded')
        else:
            speak('nothing to record')
    elif text == 'resolution':
        if url:
            w, h = img.size
            print("({},{})".format(w, h))
        else:
            speak('nothing to show')
    elif text == 'breed':
        if url:
            x=url.split('/')
            print(x[4])
            speak(x[4])
        else:
            speak('nothing to show')
    else:
        print("command not found")