"""
api_service.py — All external API logic isolated here.
Uses OpenRouter for fast cloud-based LLM (5-15 seconds response time).
"""

import json
import httpx
import logging
from app.core.config import get_settings
from app.models.schemas import (
    LearnResponse,
    QuizQuestion,
    AdaptiveQuestionRequest,
    AdaptiveQuestionResponse,
)

settings = get_settings()
logger = logging.getLogger(__name__)

# OpenRouter config (cloud-based, much faster than local)
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "gpt-3.5-turbo"  # Fast and reliable, works with OpenRouter


async def _call_openrouter(messages: list[dict]) -> str:
    """Call OpenRouter API and return response text."""
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://aitutor.app",
        "X-Title": "AITutor",
    }
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2000,
    }
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(OPENROUTER_URL, headers=headers, json=payload)
            
            if resp.status_code != 200:
                logger.error(f"OpenRouter error {resp.status_code}: {resp.text}")
                raise ValueError(f"OpenRouter returned {resp.status_code}: {resp.text}")
            
            response_text = resp.json()["choices"][0]["message"]["content"].strip()
            if not response_text:
                raise ValueError("Empty response from OpenRouter")
            return response_text
    except Exception as e:
        logger.error(f"OpenRouter error: {e}")
        raise


async def generate_learn_response(topic: str, language: str) -> LearnResponse:
    """Generate comprehensive explanation + 10 quiz questions using OpenRouter in one call."""
    logger.info(f"Generating learn response for topic: {topic}")
    
    prompt = f"""Topic: {topic}
Language: {language}

You are an expert tutor. Provide:
1. A COMPREHENSIVE explanation of {topic} with at least 4-5 key points and examples
2. Exactly 10 multiple choice quiz questions that test understanding of different aspects

The explanation should cover:
- Definition and core concepts
- Key characteristics or components
- Why this topic matters
- Real-world applications or examples
- Important distinctions or misconceptions

Make the explanation DETAILED (3-4 paragraphs minimum) so that ALL quiz questions can be directly answered from it.

Format EXACTLY:
EXPLANATION: [Your detailed, comprehensive explanation with multiple sentences and clear sections]

QUESTION 1: [Question text]
A) [option]
B) [option]
C) [option]
D) [option]
CORRECT: [A/B/C/D]

QUESTION 2: [Question text]
A) [option]
B) [option]
C) [option]
D) [option]
CORRECT: [A/B/C/D]

(Continue for QUESTION 3-10)
"""
    
    messages = [
        {
            "role": "system",
            "content": "You are an expert tutor. Provide comprehensive, detailed, accurate educational content. Explanations should be rich with examples and clear concepts. All quiz questions must be answerable directly from the explanation provided."
        },
        {"role": "user", "content": prompt}
    ]
    
    try:
        response = await _call_openrouter(messages)
        logger.info(f"Full response received, length: {len(response)}")
        
        # Parse explanation - capture entire explanation section
        explanation = ""
        if "EXPLANATION:" in response:
            exp_start = response.find("EXPLANATION:") + len("EXPLANATION:")
            exp_end = response.find("QUESTION 1:")
            explanation = response[exp_start:exp_end].strip() if exp_end > exp_start else ""
            
            # Ensure explanation is substantial
            if len(explanation) < 100:
                logger.warning(f"Short explanation received: {len(explanation)} chars")
        
        # Parse all 10 questions
        questions = []
        for q_num in range(1, 11):
            q_marker = f"QUESTION {q_num}:"
            if q_marker not in response:
                logger.warning(f"Question {q_num} not found in response")
                break
                
            q_start = response.find(q_marker) + len(q_marker)
            q_end = response.find(f"QUESTION {q_num + 1}:") if q_num < 10 else len(response)
            q_section = response[q_start:q_end].strip()
            
            lines = q_section.split('\n')
            question_text = lines[0].strip() if lines else ""
            options = []
            correct_ans = ""
            
            for line in lines[1:]:
                line = line.strip()
                if line.startswith("A)"):
                    options.append(line)
                elif line.startswith("B)"):
                    options.append(line)
                elif line.startswith("C)"):
                    options.append(line)
                elif line.startswith("D)"):
                    options.append(line)
                elif line.startswith("CORRECT:"):
                    correct_ans = line.replace("CORRECT:", "").strip()
            
            if question_text and len(options) == 4 and correct_ans in ['A', 'B', 'C', 'D']:
                correct_idx = ord(correct_ans) - ord('A')
                correct_full = options[correct_idx]
                
                quiz_q = QuizQuestion(
                    question=question_text,
                    options=options,
                    correct_answer=correct_full,
                    explanation=f"This is the correct answer to the question about {topic}.",
                    difficulty=_clamp(1 + (q_num // 2), 1, 10)  # Gradual difficulty increase
                )
                questions.append(quiz_q)
            else:
                logger.warning(f"Failed to parse question {q_num}")
        
        # Ensure we have 10 questions by generating extras if needed
        while len(questions) < 10:
            fallback_qs = _generate_fallback_questions_from_explanation(topic, explanation, len(questions) + 1)
            if fallback_qs:
                q_text, q_opts = fallback_qs[0]
                quiz_q = QuizQuestion(
                    question=q_text,
                    options=q_opts,
                    correct_answer=q_opts[0],
                    explanation=f"Based on the explanation of {topic}",
                    difficulty=_clamp(len(questions) + 1, 1, 10)
                )
                questions.append(quiz_q)
            else:
                # Last resort fallback
                quiz_q = QuizQuestion(
                    question=f"What is a key aspect of {topic}?",
                    options=[
                        f"A) {topic} is an important concept",
                        "B) It has no practical value",
                        "C) It is outdated",
                        "D) It cannot be learned"
                    ],
                    correct_answer=f"A) {topic} is an important concept",
                    explanation=f"This is a fundamental fact about {topic}.",
                    difficulty=len(questions) + 1
                )
                questions.append(quiz_q)
        
        final_explanation = explanation if explanation and len(explanation) > 50 else f"Comprehensive information about {topic}"
        
        logger.info(f"Generated {len(questions)} questions in ~10-15 seconds")
        return LearnResponse(
            topic=topic,
            explanation=final_explanation,
            quiz=questions[:10]
        )
        
    except Exception as e:
        logger.error(f"Error in generate_learn_response: {e}")
        return LearnResponse(
            topic=topic,
            explanation=f"Information about {topic}",
            quiz=[]
        )


# ── Adaptive question ──────────────────────────────────────────────────────────

def _clamp(value: int, lo: int = 1, hi: int = 10) -> int:
    return max(lo, min(hi, value))


def _target_difficulty(last_difficulty: int, was_correct: bool) -> tuple[int, str]:
    if was_correct:
        new_diff = _clamp(last_difficulty + 2)
        change = "harder"
    else:
        new_diff = _clamp(last_difficulty - 2)
        change = "easier"
    if new_diff == last_difficulty:
        change = "same"
    return new_diff, change


def _extract_sentences_from_explanation(explanation: str) -> list[str]:
    """Extract meaningful sentences from explanation for question generation."""
    import re
    # Split by common sentence endings
    sentences = re.split(r'[.!?]+', explanation)
    # Clean and filter
    sentences = [s.strip() for s in sentences if len(s.strip()) > 15]
    return sentences[:10]  # Use up to 10 sentences

def _generate_fallback_questions_from_explanation(
    topic: str, explanation: str, difficulty: int
) -> list[tuple[str, list[str]]]:
    """Generate varied fallback questions directly from explanation content."""
    
    sentences = _extract_sentences_from_explanation(explanation)
    
    if not sentences:
        sentences = [explanation]
    
    fallback_questions = []
    
    # Question type 1: Definition/Main concept
    if len(sentences) > 0:
        sentence = sentences[0]
        # Extract key noun (rough approach)
        words = [w for w in sentence.split() if len(w) > 3 and w[0].isupper()]
        key_concept = words[0] if words else topic
        fallback_questions.append((
            f"According to the explanation, what is the primary characteristic of {topic}?",
            [
                f"A) {sentence[:60]}...",
                f"B) The opposite of what was explained",
                f"C) Something not mentioned in the material",
                f"D) None of the above"
            ]
        ))
    
    # Question type 2: Specific detail from explanation
    if len(sentences) > 1:
        fallback_questions.append((
            f"Which detail about {topic} is specifically mentioned?",
            [
                f"A) {sentences[1][:60]}...",
                f"B) {sentences[0][:60]}...",
                f"C) Something completely different",
                f"D) It is not explained"
            ]
        ))
    
    # Question type 3: Implication/Application
    if len(sentences) > 2:
        fallback_questions.append((
            f"Based on the explanation of {topic}, which of these is implied?",
            [
                f"A) {sentences[2][:60]}...",
                f"B) The explanation is unclear",
                f"C) The topic is not important",
                f"D) Opposite to what's explained"
            ]
        ))
    
    # Question type 4: Comparison within topic
    if len(sentences) > 3:
        fallback_questions.append((
            f"In the context of {topic}, how are these related?",
            [
                f"A) {sentences[1][:40]}... and {sentences[3][:40]}... are connected",
                f"B) They are completely separate",
                f"C) One contradicts the other",
                f"D) They are not explained"
            ]
        ))
    
    # Question type 5: True/False concept
    if len(sentences) > 1:
        fallback_questions.append((
            f"Which statement about {topic} is correct based on the explanation?",
            [
                f"A) {sentences[0][:60]}...",
                f"B) The explanation states the opposite",
                f"C) This is not mentioned",
                f"D) All statements are false"
            ]
        ))
    
    # Question type 6: Why/How question
    if len(sentences) > 2:
        fallback_questions.append((
            f"According to the material, why is {topic} important?",
            [
                f"A) {sentences[2][:60]}...",
                f"B) It is explained as irrelevant",
                f"C) No reason is given",
                f"D) It is not important"
            ]
        ))
    
    return fallback_questions

async def generate_adaptive_question(
    req: AdaptiveQuestionRequest,
) -> AdaptiveQuestionResponse:
    """Generate adaptive question using OpenRouter - always different and relevant."""
    
    new_difficulty, difficulty_change = _target_difficulty(
        req.last_question.difficulty, req.was_correct
    )
    
    logger.info(f"Generating adaptive Q at difficulty {new_difficulty} ({difficulty_change})")
    
    # Make sure to ask for a DIFFERENT question
    prompt = f"""Topic: {req.topic}
Full explanation provided:
{req.explanation}

IMPORTANT: Generate a COMPLETELY NEW question, NOT like: "{req.last_question.question}"
Do NOT use these options: {req.last_question.options}

Difficulty: {new_difficulty}/10
Student performance: {'Got it RIGHT - ask harder question' if req.was_correct else 'Got it WRONG - ask easier question'}

Create a question that tests understanding of the explanation above.

Format EXACTLY:
QUESTION: [Your question about {req.topic}]
A) [First option - should be correct and from explanation]
B) [Second option - plausible but wrong]
C) [Third option - plausible but wrong]
D) [Fourth option - plausible but wrong]
CORRECT: [A/B/C/D]"""
    
    messages = [
        {"role": "system", "content": "You are an expert tutor. Create unique, meaningful questions that test understanding of the provided explanation. Questions must be answerable from the content given. Always make grammatical sense."},
        {"role": "user", "content": prompt}
    ]
    
    try:
        response = await _call_openrouter(messages)
        logger.info(f"Adaptive response: {response[:200]}")
        
        lines = response.strip().split('\n')
        question_text = ""
        options = []
        correct_ans = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith("QUESTION:"):
                question_text = line.replace("QUESTION:", "").strip()
            elif line.startswith("A)"):
                options.append(line)
            elif line.startswith("B)"):
                options.append(line)
            elif line.startswith("C)"):
                options.append(line)
            elif line.startswith("D)"):
                options.append(line)
            elif line.startswith("CORRECT:"):
                correct_ans = line.replace("CORRECT:", "").strip()
        
        if question_text and len(options) == 4 and correct_ans in ['A', 'B', 'C', 'D']:
            # Validate question makes sense
            if len(question_text) > 10 and '?' in question_text:
                correct_idx = ord(correct_ans) - ord('A')
                correct_full = options[correct_idx] if correct_idx < len(options) else f"{correct_ans}) answer"
                
                question = QuizQuestion(
                    question=question_text,
                    options=options,
                    correct_answer=correct_full,
                    explanation="This is the correct answer.",
                    difficulty=new_difficulty
                )
            else:
                raise ValueError("Question format invalid")
        else:
            raise ValueError("Could not parse")
            
    except Exception as e:
        logger.error(f"Adaptive Q error: {e}, using explanation-derived fallback")
        
        # Generate fallback questions directly from explanation
        fallback_questions = _generate_fallback_questions_from_explanation(
            req.topic, req.explanation, new_difficulty
        )
        
        if fallback_questions:
            import random
            question_text, options = random.choice(fallback_questions)
        else:
            # Ultimate fallback if explanation is too short
            question_text = f"What is the main topic we're studying?"
            options = [
                f"A) {req.topic}",
                "B) Something completely different",
                "C) Not specified",
                "D) None of the above"
            ]
        
        question = QuizQuestion(
            question=question_text,
            options=options,
            correct_answer=options[0],  # A is always correct in fallback
            explanation=f"This is based on the explanation provided about {req.topic}.",
            difficulty=new_difficulty
        )

    return AdaptiveQuestionResponse(
        question=question,
        difficulty_change=difficulty_change,
        new_difficulty=new_difficulty,
    )