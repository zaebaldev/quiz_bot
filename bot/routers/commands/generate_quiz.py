import logging

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.generate_quiz import QuizGenerator

MIN_QUESTIONS = 1
MAX_QUESTIONS = 10

router = Router()
logger = logging.getLogger(__name__)


class GenerateQuiz(StatesGroup):
    topic = State()
    count = State()


@router.message(Command("/generate"))
async def cmd_generate_quiz(message: types.Message, state: FSMContext):
    await message.answer("Напишите тему квиза:")
    await state.set_state(GenerateQuiz.topic)


@router.message(GenerateQuiz.topic)
async def process_topic(message: types.Message, state: FSMContext):
    await state.update_data(topic=message.text)
    await message.answer("Введите количество вопросов (от 1 до 10):")
    await state.set_state(GenerateQuiz.count)


@router.message(GenerateQuiz.count)
async def process_count(message: types.Message, state: FSMContext):
    if (
        not message.text.isdigit()
        or not MIN_QUESTIONS <= int(message.text) <= MAX_QUESTIONS
    ):
        await message.answer("Пожалуйста, введите число от 1 до 10.")
        return

    data = await state.update_data(count=int(message.text))

    await message.answer(
        f"Начинаю генерацию квиза...\n"
        f"Тема: {data['topic']}\n"
        f"Количество: {data['count']}",
    )

    quiz_generator = QuizGenerator(
        topic=data["topic"],
        count=data["count"],
    )
    question_data = await quiz_generator.generate_quiz()
    print(question_data)
    await state.clear()
