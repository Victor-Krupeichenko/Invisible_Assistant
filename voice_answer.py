import os
import threading
import pyttsx3
import simpleaudio
from pydub import AudioSegment


# voice_id: 1, 3, 5, 6
class VoiceAnswer:
    """
    Класс для озвучивания ответов с использованием голоса установленного в ОС Windows
    """

    def __init__(self, rate=180, volume=0.8, voice_id=6, answer_filename='answer_gpt.mp3'):
        """
        Инициализация голосового ответа
        :param rate: Скорость голоса
        :param volume: Громкость голоса
        :param voice_id: ID голоса
        """
        self.rate = rate
        self.volume = volume
        self.voice_id = voice_id
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)
        self.voices = list(self.engine.getProperty('voices'))
        self.engine.setProperty('voice', self.voices[self.voice_id].id)
        self.stop_event = threading.Event()

        self.answer_filename = answer_filename
        # self.language = language

    def save_answer_file(self, answer):
        """
        Сохранения текстового сообщения в файл
        :param answer: Текстовый ответ от gpt
        """
        self.engine.save_to_file(text=answer, filename=self.answer_filename)
        self.engine.runAndWait()

    def play_file_answer(self):
        """
        Воспроизведение файла с ответом от gpt
        :return объект simpleaudio с помощью которого можно управлять воспроизведением этого файла
        """
        if os.path.exists(self.answer_filename):
            audio = AudioSegment.from_file(self.answer_filename)
            play_obj = simpleaudio.play_buffer(audio.raw_data,
                                               num_channels=audio.channels,
                                               bytes_per_sample=audio.sample_width,
                                               sample_rate=audio.frame_rate)
            return play_obj
