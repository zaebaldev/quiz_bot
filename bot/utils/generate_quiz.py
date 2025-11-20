import json

import google.generativeai as genai
from core.config import settings
from schemas.question import QuestionDataClass


class QuizGenerator:
    prompt = """
        Сгенерируй {count} вопросов с четырьмя вариантами ответов в JSON-формате. Уровень сложности: {level}. Тематика: {topic}. Формат строго такой:

    {{
    "topic": "{topic}",
    "questions": [
        {{
        "question": "Текст вопроса",
        "code":"Если вопрос содержит код, то он должен быть здесь",
        "options": [
            "вариант 1",
            "вариант 2",
            "вариант 3",
            "вариант 4"
        ],
        "correct": <номер правильного ответа от 0 до 3>
        }},
        ...
    ]
    }}

    Если в вопросе есть код, поле 'question' должно содержать только текст вопроса (например, 'Что выведет код?'),
    а сам код должен быть в поле 'code' и укажи язык программирования(например, ```python\n код\n```). Если кода нет, поле 'code' должно быть null.
    Правильный ответ должен быть реалистичным, остальные — логичными, но неправильными.
    Не используй placeholder-ы. JSON должен быть полностью валидным.
    """

    def __init__(
        self,
        topic: str,
        count: int,
    ):
        self.topic = topic
        self.count = count
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        genai.configure(api_key=settings.gemini.api_key)

    def get_prompt(self) -> str:
        """Возвращает отформатированный промпт с текущими level и topic."""
        return self.prompt.format(
            topic=self.topic,
            count=self.count,
        )

    async def generate_quiz(self) -> QuestionDataClass:
        prompt = self.get_prompt()
        response = self.model.generate_content(prompt).text
        clean_response = (
            response.strip().removeprefix("```json").removesuffix("```").strip()
        )
        data_dict = json.loads(clean_response)
        question_data = QuestionDataClass(**data_dict)
        return question_data
