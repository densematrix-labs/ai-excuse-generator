"""Excuse generation service using LLM."""
import json
from typing import List
from openai import AsyncOpenAI

from app.config import get_settings
from app.schemas.excuse import Excuse, ExcuseCategory, UrgencyLevel


class ExcuseService:
    """Service for generating excuses using LLM."""
    
    def __init__(self):
        settings = get_settings()
        self.client = AsyncOpenAI(
            base_url=settings.llm_proxy_url,
            api_key=settings.llm_proxy_key,
        )
        self.model = settings.llm_model
    
    def _get_category_description(self, category: ExcuseCategory, language: str) -> str:
        """Get human-readable category description."""
        descriptions = {
            ExcuseCategory.LATE: {
                "en": "being late to work/school/an appointment",
                "zh": "上班/上学/约会迟到",
                "ja": "仕事・学校・約束に遅刻した",
                "de": "zu spät zur Arbeit/Schule/einem Termin kommen",
                "fr": "être en retard au travail/à l'école/à un rendez-vous",
                "ko": "직장/학교/약속에 늦음",
                "es": "llegar tarde al trabajo/escuela/cita",
            },
            ExcuseCategory.SICK_LEAVE: {
                "en": "taking a sick day or time off",
                "zh": "请病假或休息",
                "ja": "病気休暇を取る",
                "de": "einen Krankheitstag nehmen",
                "fr": "prendre un jour de maladie",
                "ko": "병가를 내다",
                "es": "tomar un día por enfermedad",
            },
            ExcuseCategory.DECLINE: {
                "en": "politely declining an invitation or request",
                "zh": "礼貌地拒绝邀请或请求",
                "ja": "招待や依頼を丁重に断る",
                "de": "eine Einladung oder Anfrage höflich ablehnen",
                "fr": "décliner poliment une invitation ou une demande",
                "ko": "초대나 요청을 정중히 거절",
                "es": "rechazar cortésmente una invitación o solicitud",
            },
            ExcuseCategory.FORGOT: {
                "en": "forgetting something important",
                "zh": "忘记了重要的事情",
                "ja": "大切なことを忘れた",
                "de": "etwas Wichtiges vergessen",
                "fr": "avoir oublié quelque chose d'important",
                "ko": "중요한 것을 잊어버림",
                "es": "olvidar algo importante",
            },
            ExcuseCategory.DEADLINE: {
                "en": "missing a deadline",
                "zh": "错过截止日期",
                "ja": "締め切りに間に合わなかった",
                "de": "eine Frist verpassen",
                "fr": "manquer une date limite",
                "ko": "마감일을 놓침",
                "es": "incumplir un plazo",
            },
            ExcuseCategory.MEETING: {
                "en": "missing or being late to a meeting",
                "zh": "缺席或会议迟到",
                "ja": "会議を欠席または遅刻した",
                "de": "eine Besprechung verpassen oder zu spät kommen",
                "fr": "manquer ou être en retard à une réunion",
                "ko": "회의 불참 또는 지각",
                "es": "faltar o llegar tarde a una reunión",
            },
            ExcuseCategory.HOMEWORK: {
                "en": "not completing homework or an assignment",
                "zh": "没完成作业或任务",
                "ja": "宿題や課題を完成できなかった",
                "de": "Hausaufgaben oder eine Aufgabe nicht erledigen",
                "fr": "ne pas avoir terminé ses devoirs ou un devoir",
                "ko": "숙제나 과제를 못 함",
                "es": "no completar la tarea o un trabajo",
            },
            ExcuseCategory.OTHER: {
                "en": "a general situation requiring an excuse",
                "zh": "需要借口的一般情况",
                "ja": "言い訳が必要な一般的な状況",
                "de": "eine allgemeine Situation, die eine Entschuldigung erfordert",
                "fr": "une situation générale nécessitant une excuse",
                "ko": "변명이 필요한 일반적인 상황",
                "es": "una situación general que requiere una excusa",
            },
        }
        return descriptions.get(category, descriptions[ExcuseCategory.OTHER]).get(
            language, descriptions[category]["en"]
        )
    
    def _get_urgency_instruction(self, urgency: UrgencyLevel, language: str) -> str:
        """Get urgency-specific instruction."""
        instructions = {
            UrgencyLevel.NORMAL: {
                "en": "believable and reasonable - something that could actually happen",
                "zh": "可信且合理 - 真实可能发生的事情",
                "ja": "信じられて妥当な - 実際に起こりうること",
                "de": "glaubwürdig und vernünftig - etwas, das wirklich passieren könnte",
                "fr": "crédible et raisonnable - quelque chose qui pourrait vraiment arriver",
                "ko": "믿을 수 있고 합리적인 - 실제로 일어날 수 있는 일",
                "es": "creíble y razonable - algo que podría suceder realmente",
            },
            UrgencyLevel.URGENT: {
                "en": "slightly dramatic but still plausible - emphasize urgency",
                "zh": "略显戏剧化但仍可信 - 强调紧急性",
                "ja": "少しドラマチックだが信じられる - 緊急性を強調",
                "de": "leicht dramatisch aber noch plausibel - Dringlichkeit betonen",
                "fr": "légèrement dramatique mais encore plausible - souligner l'urgence",
                "ko": "약간 극적이지만 여전히 그럴듯한 - 긴급함 강조",
                "es": "ligeramente dramático pero aún plausible - enfatizar urgencia",
            },
            UrgencyLevel.EXTREME: {
                "en": "wild and dramatic - almost unbelievable but creative and funny",
                "zh": "疯狂而戏剧化 - 几乎难以置信但有创意且有趣",
                "ja": "ワイルドでドラマチック - ほぼ信じられないが創造的で面白い",
                "de": "wild und dramatisch - fast unglaublich aber kreativ und lustig",
                "fr": "fou et dramatique - presque incroyable mais créatif et drôle",
                "ko": "극적이고 과장된 - 거의 믿기 힘들지만 창의적이고 재미있는",
                "es": "salvaje y dramático - casi increíble pero creativo y divertido",
            },
        }
        return instructions.get(urgency, instructions[UrgencyLevel.NORMAL]).get(
            language, instructions[urgency]["en"]
        )
    
    async def generate_excuses(
        self,
        category: ExcuseCategory,
        urgency: UrgencyLevel,
        context: str = "",
        language: str = "en",
    ) -> List[Excuse]:
        """Generate creative excuses using LLM."""
        category_desc = self._get_category_description(category, language)
        urgency_inst = self._get_urgency_instruction(urgency, language)
        
        language_names = {
            "en": "English",
            "zh": "Chinese (Simplified)",
            "ja": "Japanese",
            "de": "German",
            "fr": "French",
            "ko": "Korean",
            "es": "Spanish",
        }
        lang_name = language_names.get(language, "English")
        
        context_part = f"\nAdditional context from user: {context}" if context else ""
        
        prompt = f"""You are a creative excuse generator. Generate exactly 3 unique excuses for: {category_desc}

The excuses should be: {urgency_inst}
{context_part}

IMPORTANT: Generate all content in {lang_name} language.

Return a JSON array with exactly 3 objects, each with:
- "text": The excuse itself (1-3 sentences)
- "tone": A single word describing the tone (e.g., "sincere", "apologetic", "humorous", "dramatic")
- "tip": A brief delivery tip (1 short sentence)

Return ONLY the JSON array, no other text."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=1000,
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse JSON from response
        if content.startswith("```"):
            # Remove markdown code blocks
            lines = content.split("\n")
            content = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
        
        try:
            excuses_data = json.loads(content)
            excuses = [
                Excuse(
                    text=e.get("text", ""),
                    tone=e.get("tone", "neutral"),
                    tip=e.get("tip", ""),
                )
                for e in excuses_data[:3]
            ]
        except (json.JSONDecodeError, KeyError, TypeError):
            # Fallback if JSON parsing fails
            excuses = [
                Excuse(
                    text=content,
                    tone="generated",
                    tip="Use with confidence!",
                )
            ]
        
        return excuses


# Singleton instance
_excuse_service: ExcuseService | None = None


def get_excuse_service() -> ExcuseService:
    """Get excuse service singleton."""
    global _excuse_service
    if _excuse_service is None:
        _excuse_service = ExcuseService()
    return _excuse_service
