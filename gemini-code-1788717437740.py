# models.py
from typing import List
from pydantic import BaseModel, Field

class ExecutionPlan(BaseModel):
    summary_goals: List[str] = Field(description="Key learning objectives to emphasize")
    flashcard_topics: List[str] = Field(description="Core concepts requiring memory flashcards")
    quiz_topics: List[str] = Field(description="Concepts requiring multiple-choice testing")
    target_difficulty: str = Field(description="Identified difficulty level: Beginner, Intermediate, or Advanced")

class Flashcard(BaseModel):
    concept: str
    question: str
    answer: str

class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(description="Array of exactly 4 choices")
    correct_answer: str
    explanation: str

class DraftContent(BaseModel):
    summary: str
    flashcards: List[Flashcard]

class DraftAssessment(BaseModel):
    quiz: List[QuizQuestion]

class QualityAudit(BaseModel):
    passed: bool = Field(description="True if generation meets standards, False otherwise")
    feedback: str = Field(description="Specific directions for corrections if passed is False")

class FinalStudyPack(BaseModel):
    difficulty: str
    summary: str
    flashcards: List[Flashcard]
    quiz: List[QuizQuestion]