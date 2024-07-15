import asyncio
from g4f.client import Client
from g4f.errors import RetryProviderError
from asyncio import WindowsSelectorEventLoopPolicy


# gpt-4o
# gpt-3.5-turbo

class GPTClient:
    """
    Класс для работы с GPT
    """

    def __init__(self, question, model='gpt-4o'):
        """
        Инициализация GPT-клиента
        :param question: вопрос для GPT
        :param model: модель GPT, используемая в качестве распознавателя
        """
        self.question = question
        self.model = model
        self.client = Client()

    def get_response(self):
        """
        Получение текстового ответа от GPT
        :return: текстовое сообщение
        """
        try:
            asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{'role': 'user', 'content': f'{self.question}  (ответ пиши на русском языке)'}],

            )
            return response.choices[0].message.content.replace('\n\n', '\n')
        except (RetryProviderError, Exception) as exc:
            return f'Ошибка запроса к gpt: {str(exc)}'
