import os
import pyttsx3
import simpleaudio
from pydub import AudioSegment
from settings_env import rate, volume, voice_id, answer_filename


class VoiceAnswer:
    """
    Класс для озвучивания ответов с использованием голоса установленного в ОС Windows
    """

    def __init__(self, voice_rate=rate, vol=volume, v_id=voice_id, filename=answer_filename):
        """
        Инициализация голосового ответа
        :param voice_rate: Скорость голоса
        :param vol: Громкость голоса
        :param v_id: ID голоса
        """

        self.rate = voice_rate
        self.volume = vol
        self.voice_id = v_id
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)
        self.voices = list(self.engine.getProperty('voices'))
        self.engine.setProperty('voice', self.voices[self.voice_id].id)
        self.answer_filename = filename

    def save_answer_file(self, answer):
        """
        Сохранения текстового сообщения в файл
        :param answer: Текстовый ответ от gpt
        """
        self.engine.save_to_file(text=answer, filename=self.answer_filename)
        self.engine.runAndWait()

    def talk(self, talk_message):
        """
        Озвучивание текста
        :param talk_message: Текст для озвучивания
        """

        self.engine.say(talk_message)
        try:
            self.engine.runAndWait()
        except RuntimeError:
            pass

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
