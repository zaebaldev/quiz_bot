from aiogram import Router
from .generate_quiz import router as generate_quiz_router

router = Router()
router.include_routers(generate_quiz_router)
