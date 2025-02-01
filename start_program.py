import ctypes
import re
import threading
import time
import win32con
import win32gui
from pathlib import Path
from request_to_gtp import GPTClient
from speech_to_text import SpeechToTextConverter
from voice_answer import VoiceAnswer
from settings_env import (
    model, mic_id, language, rate, volume, voice_id, answer_filename, stop_word, trigger_words, exit_program,
    talk_message, hello, exit_message, icon_tray, time_out
)
from system_tray import IconTray


class Starter:
    """
    Класс, который запускает все компоненты системы собеседника
    """

    def __init__(
            self, model_gpt=model, microphone_id=mic_id, lang=language, voice_rate=rate, vol=volume,
            v_id=voice_id, filename=answer_filename, st_word=stop_word, trg_words=trigger_words,
            exit_prog=exit_program, t_message=talk_message, icon=icon_tray
    ):
        """
        Инициализация всех компонентов системы собеседника
        :param model_gpt: модель GPT, используемая в качестве распознавателя
        :param microphone_id: ID микрофона, из которого будем получать аудио
        :param lang: Язык на котором будет производиться распознание речи и сохранения файла
        :param voice_rate: Скорость голоса
        :param vol: Громкость голоса
        :param v_id: ID голоса из ОС Windows
        :param filename: Имя файла в который будет сохранен ответ
        :param st_word: Слово, которое признано остановочным для остановки озвучивания
        :param trg_words: Слова, которые будут указывать что это запрос к gpt
        :param exit_prog: Слово, которое указывает на выход из программы
        :param t_message: Сообщение, которое будет выводиться при запуске поиска ответа gpt
        :param icon: PNG файл для иконки в трее
        """
        self.model = model_gpt
        self.microphone_id = microphone_id
        self.language = lang
        self.answer_filename = filename
        self.stop_word = st_word
        self.trigger_words = trg_words
        self.exit_program = exit_prog
        self.t_message = t_message
        self.gpt_client = GPTClient(self.model)
        self.speech_to_text_converter = SpeechToTextConverter(self.microphone_id, self.language)
        self.voice_answer = VoiceAnswer(voice_rate, vol, v_id, self.answer_filename)
        self.icon_tray = IconTray(starter=self, icon=icon)
        self.place_voice = None  # будет ссылаться на объект simpleaudio для управления аудио
        self.exit_event = threading.Event()  # Флаг 'unset' - для работы основного цикла программы

    def clear_request(self, text):
        """
        Удаление слова Тригера из текста запроса
        :param text: Текст запроса
        :return: строку с очищенным запросом
        """
        pattern = fr'\b{self.trigger_words[0]}\b|\b{self.trigger_words[1]}\b'
        cleaner_text = re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
        return cleaner_text

    @staticmethod
    def check_filename(filename):
        """
        Проверяет существование звукового файла с ответом, если файл есть то его удаляет
        :param filename: Имя файла
        """
        file_path = Path(filename)
        if file_path.is_file():
            file_path.unlink()

    def play_sound(self, clear_question):
        """
        Запуск воспроизведения файла с ответом на запрос
        :param clear_question: Очищенный текст запроса
        """
        if answer := self.gpt_client.get_response(clear_question):
            self.voice_answer.save_answer_file(answer)
        self.place_voice = self.voice_answer.play_file_answer()
        self.check_filename(self.answer_filename)

    def stop_sound(self, question):
        """
        Остановка воспроизведения файла с ответом на запрос
        :param question: Текст запроса
        """
        if question == self.stop_word and self.place_voice:
            self.place_voice.stop()
            self.check_filename(self.answer_filename)

    def handle_user_request(self, question):
        """
        Обработка запроса пользователя
        :param question: Текстовый запрос
        """
        clear_question = self.clear_request(question)
        if clear_question.lower() == hello:  # hello - это ссылка на слово приветствие (изменить можно в файле .env)
            self.play_sound(clear_question)
        else:
            self.voice_answer.talk(talk_message=self.t_message)
            self.play_sound(clear_question)

    def stop_program(self):
        """
        Метод для корректного завершения программы и освобождения ресурсов.
        """
        if self.place_voice:
            self.place_voice.stop()
        self.exit_event.set()  # устанавливаем флаг выполнения в 'set' - тем самым завершаем цикл выполнения программы
        self.voice_answer.talk(talk_message=exit_message)

    def main(self):
        """
        Запуск основного цикла работы программы
        """
        threading.Thread(target=self.icon_tray.create_icon_tray, daemon=True).start()  # запускаю иконку в трей
        time.sleep(1)
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()  # получаем дескриптор консольного окна
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)  # сворачиваем консольное окно
        while not self.exit_event.is_set():  # пока флаг 'unset'
            if question := self.speech_to_text_converter.recognize_speech(timeout=time_out):
                if any(trigger.lower() in question.lower() for trigger in self.trigger_words[:-1]):
                    self.handle_user_request(question)
                elif question == self.exit_program:
                    self.stop_program()
                    break
                self.stop_sound(question)
        self.check_filename(self.answer_filename)


if __name__ == '__main__':
    Starter().main()
