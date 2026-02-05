import httpx
from app.config import get_settings
from app.schemas.excuse import ExcuseRequest, Scenario, Style

settings = get_settings()

SCENARIO_PROMPTS = {
    Scenario.SKIP_WORK: "need to skip work / call in sick",
    Scenario.AVOID_PARTY: "need to avoid/decline a social gathering or party",
    Scenario.LATE_ARRIVAL: "arrived late or will be late",
    Scenario.FORGOT_TASK: "forgot to do an assigned task",
    Scenario.CANCEL_PLANS: "need to cancel previously made plans",
    Scenario.MISS_MEETING: "missed or will miss a meeting",
    Scenario.CUSTOM: "custom situation"
}

STYLE_INSTRUCTIONS = {
    Style.SINCERE: "Write in a sincere, heartfelt, and believable tone that evokes empathy.",
    Style.PROFESSIONAL: "Write in a professional, formal, and appropriate workplace tone.",
    Style.CREATIVE: "Write in a creative, unique way with an unexpected but plausible twist.",
    Style.DRAMATIC: "Write in a dramatic, emotional, slightly exaggerated tone.",
    Style.ABSURD: "Write in an absurdly funny, obviously fake but hilarious tone."
}

LANGUAGE_INSTRUCTIONS = {
    "en": "Write the excuse in English.",
    "zh": "用中文写这个借口。",
    "ja": "この言い訳を日本語で書いてください。",
    "de": "Schreiben Sie die Entschuldigung auf Deutsch.",
    "fr": "Écrivez l'excuse en français.",
    "ko": "이 변명을 한국어로 작성해 주세요.",
    "es": "Escribe la excusa en español."
}


class ExcuseService:
    def __init__(self):
        self.llm_url = f"{settings.llm_proxy_url}/v1/chat/completions"
        self.api_key = settings.llm_proxy_key
    
    async def generate_excuse(self, request: ExcuseRequest) -> str:
        """Generate an excuse using LLM."""
        scenario_desc = SCENARIO_PROMPTS.get(request.scenario, "custom situation")
        if request.scenario == Scenario.CUSTOM and request.custom_scenario:
            scenario_desc = request.custom_scenario
        
        style_instruction = STYLE_INSTRUCTIONS.get(request.style, STYLE_INSTRUCTIONS[Style.SINCERE])
        lang_instruction = LANGUAGE_INSTRUCTIONS.get(request.language, LANGUAGE_INSTRUCTIONS["en"])
        
        target = request.target_person or "someone"
        urgency_desc = ["very low", "low", "medium", "high", "very high"][request.urgency - 1]
        
        prompt = f"""You are an expert excuse generator. Generate a perfect excuse for the following situation:

Situation: I {scenario_desc}
Who I'm telling: {target}
Urgency level: {urgency_desc}

{style_instruction}
{lang_instruction}

Requirements:
- Keep it concise (2-4 sentences)
- Make it specific and detailed enough to be believable
- Match the tone to the style requested
- Do not include any meta-commentary, just the excuse itself

Generate the excuse now:"""

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.llm_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gemini-2.5-flash",
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant that generates creative and believable excuses."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 300,
                    "temperature": 0.8
                }
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
