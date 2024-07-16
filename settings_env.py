import os
from dotenv import load_dotenv

load_dotenv()

model = os.getenv('MODEL').split(',')
mic_id = int(os.getenv('MICROPHONE_ID'))
language = os.getenv('LANGUAGE')
rate = int(os.getenv('RATE'))
volume = float(os.getenv('VOLUME'))
voice_id = list(map(int, os.getenv('voice_id').split(',')))
answer_filename = os.getenv('ANSWER_FILENAME')
stop_word = os.getenv('STOP_WORD')
trigger_words = os.getenv('TRIGGER_WORDS').split(',')
exit_program = os.getenv('EXIT_PROGRAM')
