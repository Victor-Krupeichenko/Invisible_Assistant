import speech_recognition as sr


class SpeechToTextConverter:
    """
    Класс распознания речи и конвертации ее в текст
    """

    def __init__(self, microphone_id=0, language='ru'):
        """
        Инициализация распознавателя речи
        :param microphone_id: ID микрофона, из которого будем получать аудио
        :param language: Язык на котором будет производиться распознание речи
        """
        self.microphone_id = microphone_id
        self.language = language
        self.r = sr.Recognizer()
        self.mic = sr.Microphone(device_index=microphone_id)

    def recognize_speech(self):
        """
        Распознаем голос и вернем текст, сгенерированный распознавателем речи
        :return: текст, распознанный голосом
        """
        with self.mic as source:
            self.r.energy_threshold = 15000
            self.r.adjust_for_ambient_noise(source, duration=.5)
            print("Слушаю...")
            audio = self.r.listen(source)
            try:
                text_recognition = self.r.recognize_google(audio, language=self.language)
                return text_recognition
            except sr.UnknownValueError as exc:
                print(f'Распознание речи не удалось {exc}')
            except sr.RequestError as exc:
                print(f'Не удалось запросить результаты от службы распознавания речи Google. {exc}')
            return None
