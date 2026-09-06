# prompts.py
# System prompts and template definitions for each stage of the AI Study Pack Generator

PLANNING_PROMPT_TEMPLATE = """
Analyze these study notes and construct a structural learning plan:

{notes}
"""

CONTENT_PROMPT_TEMPLATE = """
Generate a comprehensive summary and detailed flashcards.
Plan Goals: {summary_goals}
Flashcard Topics: {flashcard_topics}
Target Difficulty: {target_difficulty}

Notes:
{notes}
"""

ASSESSMENT_PROMPT_TEMPLATE = """
Create 4-option practice quiz questions based on these topics: {quiz_topics}.
Target Difficulty: {target_difficulty}

Notes:
{notes}
"""

AUDIT_PROMPT_TEMPLATE = """
Audit the generated content against the original study notes for accuracy, completeness, and clarity.

Original Notes:
{notes}

Generated Summary:
{summary}

Generated Flashcards:
{flashcards}

Generated Quiz:
{quiz}

Set passed=true if acceptable. Set passed=false and state clear feedback if flashcards or quiz items are inaccurate or lacking depth.
"""

REFINEMENT_PROMPT_TEMPLATE = """
Fix and rewrite the summary and flashcards using this feedback: {feedback}

Original Notes:
{notes}
"""
