import asyncio
from g4f.client import Client
from g4f.errors import RetryProviderError
from asyncio import WindowsSelectorEventLoopPolicy
from settings_env import model


class GPTClient:
    """
    Класс для работы с GPT API
    """

    def __init__(self, model_gpt=model):
        """
        Инициализация GPT-клиента
        :param model_gpt: модель GPT, используемая в качестве распознавателя
        """
        self.model = model_gpt
        self.client = Client()

    def get_response(self, question):
        """
        Получение текстового ответа от GPT
        :return: текстовое сообщение
        """
        try:
            asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{'role': 'user', 'content': f'{question}  (ответ пиши только на русском языке)'}],
                # TODO добавить от какого лица писать (женского/мужского) в зависимости от выбранного голоса
            )
            clear_response = response.choices[0].message.content.replace('\n\n', '\n')
            print(clear_response)
            if 'BLACKBOX.AI' in clear_response or 'Model not found or too long input' in clear_response:
                return 'Повторите запрос'
            return clear_response
        except (RetryProviderError, Exception) as exc:
            return f'Ошибка запроса к gpt: {str(exc)}'
