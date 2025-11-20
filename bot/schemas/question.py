from dataclasses import dataclass
from typing import NotRequired, TypedDict


class QuestionDict(TypedDict):
    question: str
    code: NotRequired[str]
    options: list[str]
    correct: int


@dataclass
class QuestionDataClass:
    level: str
    questions: list[QuestionDict]
    topic: str | None = None
