import yaml
import torch
from faster_whisper import WhisperModel
from gtts import gTTS
import os
import time

def open_data(file_path):
    i = 0
    while i < 3:
        i = i + 1
        time.sleep(0.1)
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            if config is not None:
                break
    return config

def update_data(file_path, data):
    if file_path != "users/000000.yaml":
        with open(file_path, 'w') as file:
            yaml.dump(data, file)

def clean_text(string):
    string = string.lower()
    string = " ".join(string.split())
    string = string.strip()
    chars = '"\'“¿([{-"\'.。|,，!！?？:：”)]}、'
    for char in chars:
        string = string.replace(char, "")
    return string

def voice2text(v2t, audio_file, model_size):
    if v2t != 'OpenAI':
        if torch.cuda.is_available():
            model = WhisperModel(model_size, device="cuda", compute_type="float16")
        else:
            model = WhisperModel(model_size, device="cpu", compute_type="int8")
        segments, info = model.transcribe(audio_file)
        result = ''.join([segment.text for segment in segments])
        return result

def text2voice(t2v, user, text, lang, voice, speed):
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    if not os.path.exists(f'tmp/{user}'):
        os.makedirs(f'tmp/{user}')

    if t2v == 'gTTS':
        speed = round(speed * 2, 1) / 2
        tts = gTTS(text, lang=lang)
        tts.save(f'tmp/{user}/t2v.mp3')
        cmd = f"ffmpeg -loglevel quiet -i 'tmp/{user}/t2v.mp3' -filter:a \"atempo={speed}\" -vn tmp/{user}/t2v_.mp3 -y"
        os.system(cmd)
        os.rename(f'tmp/{user}/t2v_.mp3', f'tmp/{user}/t2v.mp3')
