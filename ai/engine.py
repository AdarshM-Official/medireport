import os
import json
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from .prompts import SYSTEM_PROMPT

def analyze_medical_text(text):
    if not text or len(text.strip()) < 10:
        return {
            "summary": "The uploaded file does not contain any readable text. Please ensure you upload a clear image or PDF of a lab result.",
            "insights": [],
            "all_findings": [],
            "recommendations": []
        }

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        # Fallback for demonstration if API key is missing
        return {
            "summary": "Demo Mode: No OPENROUTER_API_KEY provided in the environment. This is a placeholder summary.",
            "abnormalities": [
                {
                    "parameter": "API Key Missing",
                    "value": "N/A",
                    "reference_range": "N/A",
                    "severity": "Attention",
                    "explanation": "Please add an OPENROUTER_API_KEY to your environment variables to enable real AI analysis."
                }
            ],
            "recommendations": ["Set OPENROUTER_API_KEY environment variable."]
        }
    
    if not OpenAI:
        return {"summary": "Error: openai package is not installed.", "abnormalities": [], "recommendations": []}

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"Error calling OpenRouter API: {e}")
        return {
            "summary": "Failed to analyze report due to an AI service error.",
            "abnormalities": [],
            "recommendations": []
        }
