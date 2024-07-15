import re
import os
from request_to_gtp import GPTClient
from speech_to_text import SpeechToTextConverter
from voice_answer import VoiceAnswer


class Starter:
    """
    Класс, который запускает все компоненты системы собеседника
    """

    def __init__(
            self, model='gpt-4o', microphone_id=0, language='ru', rate=180, volume=0.8, voice_id=6,
            answer_filename='answer_gpt.mp3', stop_word='остановись', trigger_words=('Bobby', 'Бобби')
    ):
        """
        Инициализация всех компонентов системы собеседника
        :param model: модель GPT, используемая в качестве распознавателя
        :param microphone_id: ID микрофона, из которого будем получать аудио
        :param language: Язык на котором будет производиться распознание речи и сохранения файла
        :param rate: Скорость голоса
        :param volume: Громкость голоса
        :param voice_id: ID голоса из ОС Windows
        :param answer_filename: Имя файла в который будет сохранен ответ
        :param stop_word: Слово, которое признано остановочным для остановки озвучивания
        :param trigger_words: Слова, которые будут указывать что это запрос к gpt
        """
        self.model = model
        self.microphone_id = microphone_id
        self.language = language
        self.answer_filename = answer_filename
        self.stop_word = stop_word
        self.trigger_words = trigger_words
        self.gpt_client = GPTClient(self.model)
        self.speech_to_text_converter = SpeechToTextConverter(self.microphone_id, self.language)
        self.voice_answer = VoiceAnswer(rate, volume, voice_id, self.answer_filename)
        self.place_voice = None

    def clear_request(self, text):
        """
        Удаление слова Тригера из текста запроса
        :param text: Текст запроса
        :return: строку с очищенным запросом
        """
        pattern = fr'\b{self.trigger_words[0]}\b|\b{self.trigger_words[1]}\b'
        cleaner_text = re.sub(pattern, '', text).strip()
        return cleaner_text

    def play_sound(self, question):
        """
        Запуск воспроизведения файла с ответом на запрос
        :param question: Текст запроса
        """
        if answer := self.gpt_client.get_response(self.clear_request(question)):
            print(answer)
            self.voice_answer.save_answer_file(answer)
        self.place_voice = self.voice_answer.play_file_answer()

    def stop_sound(self, question):
        """
        Остановка воспроизведения файла с ответом на запрос
        :param question: Текст запроса
        """
        if question == self.stop_word:
            self.place_voice.stop()
            os.remove(self.answer_filename)

    def main(self):
        """
        Запуск системы собеседника
        """
        while True:
            if question := self.speech_to_text_converter.recognize_speech():
                if any(trigger in question for trigger in self.trigger_words):
                    self.play_sound(question)
                elif question == 'выход':
                    break
                self.stop_sound(question)


if __name__ == '__main__':
    # starter = Starter()
    # starter = Starter(model='gpt-3.5-turbo', voice_id=1)
    starter = Starter(model='gpt-3.5-turbo')
    starter.main()
