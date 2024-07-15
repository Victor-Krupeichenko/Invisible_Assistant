import pyttsx3


# voice_id: 1, 3, 5, 6
class VoiceAnswer:
    """
    Класс для озвучивания ответов с использованием голоса установленного в ОС Windows
    """

    def __init__(self, rate=180, volume=0.8, voice_id=6):
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

    def voice_message(self, message):
        """
        Генерация голосового сообщения
        :param message: Сообщение для голосового ответа
        """
        try:
            self.engine.say(message)
        except Exception as exc:
            print(f'Ошибка голосового ответа: {exc}')
