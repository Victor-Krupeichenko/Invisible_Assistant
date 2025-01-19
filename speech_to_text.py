import sys
import speech_recognition as sr
from settings_env import mic_id, language


class SpeechToTextConverter:
    """
    Класс распознания речи и конвертации ее в текст
    """

    def __init__(self, microphone_id=mic_id, lang=language):
        """
        Инициализация распознавателя речи
        :param microphone_id: ID микрофона, из которого будем получать аудио
        :param lang: Язык на котором будет производиться распознание речи
        """
        self.microphone_id = microphone_id
        self.language = lang
        self.r = sr.Recognizer()
        self.mic = sr.Microphone(device_index=microphone_id)

    def recognize_speech(self, timeout=None):
        """
        Распознаем голос и вернем текст, сгенерированный распознавателем речи
        :param timeout: Время ожидания начало фразы, по истечении которого распознавание прекращается, в секундах
        :return: текст, распознанный голосом или None
        """
        with self.mic as source:
            self.r.energy_threshold = 16000
            self.r.adjust_for_ambient_noise(source, 1.2)
            sys.stdout.write(f"\rСлушаю...") # Выводим сообщение о начале прослушания
            sys.stdout.flush()
            try:
                audio = self.r.listen(source, timeout=timeout)
                text_recognition = self.r.recognize_google(audio, language=self.language)
                return text_recognition
            except sr.UnknownValueError:
                # TODO придумать что делать с исключениями в место pass
                pass
                # print(f'Распознание речи не удалось {exc}')
            except sr.RequestError:
                pass
                # print(f'Не удалось запросить результаты от службы распознавания речи Google. {exc}')
            except sr.WaitTimeoutError:
                pass
                # print(f'Превышено время ожидания. {exc}')
            return None
