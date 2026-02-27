"""
true_false_service.py — Generate True/False statements from explanations
"""

import logging
import httpx
from app.core.config import get_settings
from app.models.schemas import (
    TrueOrFalseResponse,
    TrueOrFalseStatement,
)

settings = get_settings()
logger = logging.getLogger(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "gpt-3.5-turbo"


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
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(OPENROUTER_URL, headers=headers, json=payload)
            
            if resp.status_code != 200:
                logger.error(f"OpenRouter error {resp.status_code}: {resp.text}")
                raise ValueError(f"OpenRouter returned {resp.status_code}: {resp.text}")
            
            response_text = resp.json()["choices"][0]["message"]["content"].strip()
            if not response_text:
                raise ValueError("Empty response from OpenRouter")
            return response_text
    except httpx.TimeoutException:
        raise ValueError("OpenRouter request timed out")
    except Exception as e:
        logger.error(f"OpenRouter error: {e}")
        raise


async def generate_true_false_statements(
    topic: str,
    explanation: str,
    language: str = "en"
) -> TrueOrFalseResponse:
    """Generate 10 True/False statements from the explanation for swipeable cards."""
    
    logger.info(f"Generating True/False statements for topic: {topic}")
    
    prompt = f"""Topic: {topic}
Explanation:
{explanation}

Language: {language}

Create 10 True/False statements that test understanding of the explanation above.

Requirements:
- Mix of TRUE and FALSE statements (5 true, 5 false)
- Statements should be based on facts in the explanation
- Some TRUE statements should be directly from explanation
- Some FALSE statements should be plausible misconceptions
- Each should have a brief explanation of why it's true/false
- Statements should be concise (1-2 sentences max)
- Statements must be directly evaluable as TRUE or FALSE

Format EXACTLY (with no extra text):
STATEMENT 1: [A statement about {topic}]
IS_TRUE: [TRUE/FALSE]
REASON: [Brief explanation why it's true or false]

STATEMENT 2: [A statement about {topic}]
IS_TRUE: [TRUE/FALSE]
REASON: [Brief explanation why it's true or false]

(Continue for STATEMENT 3-10, alternating between TRUE and FALSE)
"""
    
    messages = [
        {
            "role": "system",
            "content": "You are an expert educator. Create clear, evaluable True/False statements that test understanding of the provided material. Mix TRUE and FALSE statements. Each statement must be definitely TRUE or FALSE based on the explanation."
        },
        {"role": "user", "content": prompt}
    ]
    
    try:
        response = await _call_openrouter(messages)
        logger.info(f"True/False response received, length: {len(response)}")
        
        statements = []
        
        # Parse all 10 statements
        for stmt_num in range(1, 11):
            stmt_marker = f"STATEMENT {stmt_num}:"
            if stmt_marker not in response:
                logger.warning(f"Statement {stmt_num} not found")
                break
            
            stmt_start = response.find(stmt_marker) + len(stmt_marker)
            stmt_end = response.find(f"STATEMENT {stmt_num + 1}:") if stmt_num < 10 else len(response)
            stmt_section = response[stmt_start:stmt_end].strip()
            
            lines = stmt_section.split('\n')
            statement_text = lines[0].strip() if lines else ""
            is_true_str = ""
            reason = ""
            
            for line in lines[1:]:
                line = line.strip()
                if line.startswith("IS_TRUE:"):
                    is_true_str = line.replace("IS_TRUE:", "").strip().upper()
                elif line.startswith("REASON:"):
                    reason = line.replace("REASON:", "").strip()
            
            # Validate
            if statement_text and is_true_str in ["TRUE", "FALSE"] and reason:
                is_true = is_true_str == "TRUE"
                stmt = TrueOrFalseStatement(
                    id=stmt_num,
                    statement=statement_text,
                    is_true=is_true,
                    explanation=reason
                )
                statements.append(stmt)
                logger.info(f"Statement {stmt_num}: Parsed ({is_true_str})")
            else:
                logger.warning(f"Failed to parse statement {stmt_num}")
        
        # Fallback if parsing fails
        if len(statements) < 10:
            logger.warning(f"Only got {len(statements)} statements, generating fallbacks")
            # Generate simple fallback statements from explanation
            words = explanation.split()
            if len(words) > 20:
                sample_text = " ".join(words[:20])
                for i in range(len(statements), 10):
                    stmt = TrueOrFalseStatement(
                        id=i + 1,
                        statement=f"The explanation mentions key aspects of {topic}.",
                        is_true=i % 2 == 0,  # Alternate true/false
                        explanation="This relates to the explanation provided."
                    )
                    statements.append(stmt)
        
        return TrueOrFalseResponse(
            topic=topic,
            statements=statements[:10]
        )
        
    except Exception as e:
        logger.error(f"Error in generate_true_false_statements: {e}")
        # Return empty response on error - frontend will handle gracefully
        return TrueOrFalseResponse(
            topic=topic,
            statements=[]
        )
