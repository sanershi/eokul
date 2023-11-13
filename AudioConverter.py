import speech_recognition as sr
from speech_recognition.exceptions import UnknownValueError
import pydub
import io
import os
from colorama import Fore

pydub.AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
pydub.AudioSegment.ffmpeg = r"C:\ffmpeg\bin\ffmpeg.exe"
pydub.AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

RECOGNIZER = sr.Recognizer()
TABLE = {
    "bir": "1",
    "iki": "2",
    "üç": "3",
    "dört": "4",
    "beş": "5",
    "altı": "6",
    "yedi": "7",
    "sekiz": "8",
    "dokuz": "9",
    "sıfır": "0"
}


# convert ogg to wav
def convert_ogg_raw_to_wav(raw_ogg):
    raw_ogg_data = raw_ogg

    ogg_audio = pydub.AudioSegment.from_file(
        io.BytesIO(raw_ogg_data), format='ogg')

    raw_wav_data = ogg_audio.export(format='wav', parameters=[
                                    '-f', 's16le', '-ac', '1', '-ar', '44100'], codec='pcm_s16le', bitrate='705')

    raw_wav_data = raw_wav_data.read()

    return raw_wav_data


# convert audio to text
def recognize_raw_wav(raw_wav):
    audio_data = sr.AudioData(raw_wav, sample_rate=44100,
                              sample_width=2)
    #e3xco.d@e always win! :)
    audio_data.channels = 1

    try:
        text = RECOGNIZER.recognize_google(
            audio_data, language="tr-TR").replace(" ", "")
    except UnknownValueError as e:
        print(Fore.RED + "Alınan ses datası hatalı çıktı yeniden deneniyor !" + Fore.RESET)
        return False

    text = check_fix_recognition(text)

    return text


# test recognition result and fix
def check_fix_recognition(captcha_code):

    if not str(captcha_code).isnumeric():
        # debug
        print(f"Corrupted Recognition : {captcha_code}")

        captcha_code = multi_replacer(captcha_code.lower())

        # debug
        print(f"Fixed Recognition : {repr(captcha_code)}")

    length = len(str(captcha_code))
    if length != 4:
        captcha_code = False

    return captcha_code


# string code fixer
def multi_replacer(text):
    for k, r in TABLE.items():
        text = text.replace(k, r)
    return text


# direct get captcha code
def direct_get_from_ogg(raw_ogg):
    raw_wav_data = convert_ogg_raw_to_wav(raw_ogg)
    captcha_code = recognize_raw_wav(raw_wav_data)
    return captcha_code
