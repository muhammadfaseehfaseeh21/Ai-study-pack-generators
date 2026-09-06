# workflow.py
import json
from google import genai
from google.genai import types
from models import ExecutionPlan, DraftContent, DraftAssessment, QualityAudit
import prompts

class StudyPackOrchestrator:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model = 'gemini-3.5-flash'
    def run_stage_planning(self, notes: str) -> ExecutionPlan:
        prompt = prompts.PLANNING_PROMPT_TEMPLATE.format(notes=notes)
        res = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ExecutionPlan
            )
        )
        return ExecutionPlan.model_validate_json(res.text)

    def run_stage_content(self, notes: str, plan: ExecutionPlan) -> DraftContent:
        prompt = prompts.CONTENT_PROMPT_TEMPLATE.format(
            summary_goals=plan.summary_goals,
            flashcard_topics=plan.flashcard_topics,
            target_difficulty=plan.target_difficulty,
            notes=notes
        )
        res = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=DraftContent
            )
        )
        return DraftContent.model_validate_json(res.text)

    def run_stage_assessment(self, notes: str, plan: ExecutionPlan) -> DraftAssessment:
        prompt = prompts.ASSESSMENT_PROMPT_TEMPLATE.format(
            quiz_topics=plan.quiz_topics,
            target_difficulty=plan.target_difficulty,
            notes=notes
        )
        res = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=DraftAssessment
            )
        )
        return DraftAssessment.model_validate_json(res.text)

    def run_stage_audit(self, notes: str, content: DraftContent, assessment: DraftAssessment) -> QualityAudit:
        prompt = prompts.AUDIT_PROMPT_TEMPLATE.format(
            notes=notes,
            summary=content.summary,
            flashcards=json.dumps([f.model_dump() for f in content.flashcards]),
            quiz=json.dumps([q.model_dump() for q in assessment.quiz])
        )
        res = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=QualityAudit
            )
        )
        return QualityAudit.model_validate_json(res.text)

    def run_stage_refinement(self, notes: str, feedback: str) -> DraftContent:
        prompt = prompts.REFINEMENT_PROMPT_TEMPLATE.format(
            feedback=feedback,
            notes=notes
        )
        res = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=DraftContent
            )
        )
        return DraftContent.model_validate_json(res.text)
