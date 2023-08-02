import speech_recognition as sr
from telebot import types
import soundfile as sf
import urllib.request
import subprocess
import requests
import telebot
import json
import os

TOKEN=''
bot = telebot.TeleBot(TOKEN)
s = requests.session()

def wav2text(dest_filename, id, file_name):
    r = sr.Recognizer()
    message = sr.AudioFile(dest_filename)

    with message as source:
        audio = r.record(source)
    try:
        result = r.recognize_google(audio, language="ru_RU")
        bot.send_message(id, format(result))
        os.remove(dest_filename)
        os.remove(file_name)

    except sr.UnknownValueError:
        bot.send_message(id, 'Не удалось распознать текст')
        os.remove(dest_filename)
        os.remove(file_name)

def oga2wav(file_name, id):
    src_filename = file_name
    dest_filename = file_name + '.wav'
    process = subprocess.run(['ffmpeg', '-i', src_filename, dest_filename])
    wav2text(dest_filename, id, file_name)

def donwload(file_path, file_id, id):
    url = 'https://api.telegram.org/file/bot5176992957:AAE6oX7SdfJxGULiO9MS1uEpbviTmLyXxvg/' + file_path
    urllib.request.urlretrieve(url, file_id + '.oga')
    file_name = file_id + '.oga'
    oga2wav(file_name, id)

def request2text(file_id, id):
    r = s.get('https://api.telegram.org/bot5176992957:AAE6oX7SdfJxGULiO9MS1uEpbviTmLyXxvg/getFile?file_id=' + file_id)
    r = json.loads(r.text)

    donwload(r['result']['file_path'], r['result']['file_id'], id)

@bot.message_handler(content_types=['text'])
def start_message(message):
    bot.send_message(message.chat.id, 'Пришли / Перешли мне любое аудиосообщение')

@bot.message_handler(content_types=['voice'])
def start_message(message):
    request2text(message.voice.file_id, message.chat.id)

bot.polling()