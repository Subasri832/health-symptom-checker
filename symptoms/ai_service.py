import os
from groq import Groq
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def translate_to_english(text: str, source_lang: str = "ta") -> str:
    """Translate Tamil or any language to English"""
    try:
        translator = GoogleTranslator(source=source_lang, target="en")
        return translator.translate(text)
    except Exception:
        return text


def translate_to_tamil(text: str) -> str:
    """Translate English response to Tamil"""
    try:
        translator = GoogleTranslator(source="en", target="ta")
        return translator.translate(text)
    except Exception:
        return text


def analyze_symptoms(symptoms_text: str, language: str = "en", conversation_history: list = None) -> dict:
    """
    Main AI function that analyzes symptoms and returns diagnosis
    """

    # Translate to English if Tamil input
    if language == "ta":
        symptoms_english = translate_to_english(symptoms_text, source_lang="ta")
    else:
        symptoms_english = symptoms_text

    # Build conversation history for context
    messages = [
        {
            "role": "system",
            "content": """You are an experienced medical AI assistant. 
            Analyze the patient's symptoms and provide:
            
            1. POSSIBLE CONDITIONS: List 2-3 possible medical conditions
            2. SEVERITY: Rate as exactly one of: mild / moderate / serious
            3. RECOMMENDED SPECIALIST: Which doctor to see (e.g., General Physician, Cardiologist)
            4. IMMEDIATE ADVICE: What to do right now
            5. FOLLOW UP QUESTIONS: Ask 2 clarifying questions to better understand
            
            Format your response EXACTLY like this:
            
            POSSIBLE CONDITIONS: [condition1, condition2]
            SEVERITY: [mild/moderate/serious]
            RECOMMENDED SPECIALIST: [specialist name]
            IMMEDIATE ADVICE: [advice here]
            FOLLOW UP QUESTIONS: [question1] | [question2]
            
            IMPORTANT: 
            - Always recommend seeing a real doctor
            - Never diagnose definitively
            - Be empathetic and clear
            - Keep response concise
            """
        }
    ]

    # Add conversation history if exists
    if conversation_history:
        messages.extend(conversation_history)

    # Add current symptoms
    messages.append({
        "role": "user",
        "content": f"Patient symptoms: {symptoms_english}"
    })

    # Call Groq API
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.3,
        max_tokens=800
    )

    ai_response = response.choices[0].message.content

    # Parse the response
    result = parse_ai_response(ai_response)

    # Translate back to Tamil if needed
    if language == "ta":
        result["ai_diagnosis"] = translate_to_tamil(result["ai_diagnosis"])
        result["immediate_advice"] = translate_to_tamil(result["immediate_advice"])
        result["follow_up_questions"] = translate_to_tamil(result["follow_up_questions"])

    return result


def parse_ai_response(response_text: str) -> dict:
    """Parse the structured AI response into a dictionary"""
    result = {
        "ai_diagnosis": response_text,
        "severity": "mild",
        "recommended_speciality": "general",
        "immediate_advice": "",
        "follow_up_questions": "",
        "possible_conditions": []
    }

    lines = response_text.split('\n')

    for line in lines:
        line = line.strip()

        if line.startswith("SEVERITY:"):
            severity = line.replace("SEVERITY:", "").strip().lower()
            if "serious" in severity:
                result["severity"] = "serious"
            elif "moderate" in severity:
                result["severity"] = "moderate"
            else:
                result["severity"] = "mild"

        elif line.startswith("RECOMMENDED SPECIALIST:"):
            specialist = line.replace("RECOMMENDED SPECIALIST:", "").strip().lower()
            speciality_map = {
                "general": "general",
                "cardiologist": "cardiologist",
                "dermatologist": "dermatologist",
                "neurologist": "neurologist",
                "orthopedic": "orthopedic",
                "pediatrician": "pediatrician",
                "psychiatrist": "psychiatrist",
                "gynecologist": "gynecologist",
                "ent": "ent",
                "ophthalmologist": "ophthalmologist",
                "gastroenterologist": "gastroenterologist",
                "pulmonologist": "pulmonologist",
            }
            for key, value in speciality_map.items():
                if key in specialist:
                    result["recommended_speciality"] = value
                    break

        elif line.startswith("IMMEDIATE ADVICE:"):
            result["immediate_advice"] = line.replace("IMMEDIATE ADVICE:", "").strip()

        elif line.startswith("FOLLOW UP QUESTIONS:"):
            result["follow_up_questions"] = line.replace("FOLLOW UP QUESTIONS:", "").strip()

        elif line.startswith("POSSIBLE CONDITIONS:"):
            conditions_str = line.replace("POSSIBLE CONDITIONS:", "").strip()
            conditions_str = conditions_str.strip("[]")
            result["possible_conditions"] = [c.strip() for c in conditions_str.split(",")]

    return result


def get_severity_color(severity: str) -> str:
    """Return color code based on severity"""
    colors = {
        "mild": "#22c55e",
        "moderate": "#f59e0b",
        "serious": "#ef4444"
    }
    return colors.get(severity, "#22c55e")


def get_severity_emoji(severity: str) -> str:
    """Return emoji based on severity"""
    emojis = {
        "mild": "🟢",
        "moderate": "🟡",
        "serious": "🔴"
    }
    return emojis.get(severity, "🟢")