import speech_recognition as sr
import os
import sys

r = sr.Recognizer()

os.system('ffmpeg -i media/audio.aac media/audio.wav && rm media/audio.aac')
print("running sr")

with sr.AudioFile("media/audio.wav") as source:
        audioData = r.record(source)
        text      = r.recognize_sphinx(audioData, language="es")

with open("media/srtext.txt", "w+") as f:
    f.write(text)


os.system("rm media/audio.wav")
sys.exit(text)
