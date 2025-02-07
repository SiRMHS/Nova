import os 
import queue 
import pyaudio 
import tkinter as tk
import threading
from google.cloud import speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

RATE = 16000
CHUNK = int(RATE/10)

audio_queue = queue.Queue()
 
client = speech.SpeechClient()

# داده هارو از میکروفون میگیریم میزاریم تو صف
def record_callback(in_data , frame_count , time_info , status):
    audio_queue.put(in_data)
    return (None , pyaudio.paContinue)


# داده های صوتی رو از صف بفرسته به Api
def audio_generator():
    while True:
        chunk = audio_queue.get()
        if chunk is None:
            return
        yield speech.StreamingRecognizeRequest(audio_content = chunk)

# گوش دادن به میکروفون
def listen():
    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format= pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=record_callback,
    )

    print("🎤 lotfan Sohbat kon...")

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="fa-IR", 
        enable_automatic_punctuation=True  
    )

    stream_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    responses = client.streaming_recognize(stream_config , audio_generator())

    for response in responses:
        for result in response.results:
            text = result.alternatives[0].transcript
            print(text)


listen()