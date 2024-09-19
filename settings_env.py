import os
from dotenv import load_dotenv

load_dotenv()

model = os.getenv('MODEL')
mic_id = int(os.getenv('MICROPHONE_ID'))
language = os.getenv('LANGUAGE')
rate = int(os.getenv('RATE'))
volume = float(os.getenv('VOLUME'))
voice_id = int(os.getenv('VOICE_ID'))
answer_filename = os.getenv('ANSWER_FILENAME')
stop_word = os.getenv('STOP_WORD')
trigger_words = os.getenv('TRIGGER_WORDS').split(',')
exit_program = os.getenv('EXIT_PROGRAM')
talk_message = os.getenv('TALK_MESSAGE')
hello = os.getenv('HELLO')
exit_message = os.getenv('EXIT_MESSAGE')
icon_tray = os.getenv('ICON_TRAY')
time_out = float(os.getenv('TIME_OUT'))
