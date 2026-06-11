# src/services/llm_service.py

import json
import asyncio
import dashscope
import re
from src.prompts.templates import SYSTEM_PROMPT, ROUTE_PROMPT, SUGGESTION_PROMPT

class LLMService:
    def __init__(self, api_key=None):
        if api_key:
            dashscope.api_key = api_key
        self.model = "qwen2.5-14b-instruct"

    async def chat_with_sentiment(self, message, context=None):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ]
        if context:
            messages.insert(1, {"role": "system", "content": f"参考知识: {context}"})

        response = await asyncio.to_thread(
            dashscope.Generation.call,
            model=self.model,
            messages=messages,
            result_format="message"
        )

        if response.status_code != 200:
            return {
                "answer": "抱歉，我现在无法回答。请稍后再试。",
                "sentiment": "中性",
                "confidence": 0.0,
                "error": response.message
            }

        raw_text = response.output.choices[0].message.content
        answer, sentiment_data = self._parse_sentiment(raw_text)

        return {
            "answer": answer,
            "sentiment": sentiment_data.get("sentiment", "中性"),
            "confidence": sentiment_data.get("confidence", 0.5)
        }

    async def generate_route(self, user_profile):
        prompt = ROUTE_PROMPT.format(**user_profile)
        response = await asyncio.to_thread(
            dashscope.Generation.call,
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            result_format="message"
        )
        
        if response.status_code != 200:
            return {"error": response.message}
        
        try:
            return json.loads(response.output.choices[0].message.content)
        except (json.JSONDecodeError, AttributeError) as e:
            return {"error": f"路线生成解析失败: {str(e)}"}

    async def generate_suggestions(self, report_data):
        prompt = SUGGESTION_PROMPT.format(**report_data)
        response = await asyncio.to_thread(
            dashscope.Generation.call,
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            result_format="message"
        )
        
        if response.status_code != 200:
            return []
        
        try:
            return json.loads(response.output.choices[0].message.content).get("suggestions", [])
        except (json.JSONDecodeError, AttributeError):
            return []

    def _parse_sentiment(self, text):
        pattern = r'###sentiment###(\{.*?\})'
        match = re.search(pattern, text)
        if match:
            try:
                sentiment_json = match.group(1).replace("'", "\"") # Ensure valid JSON
                sentiment_data = json.loads(sentiment_json)
                answer = text[:match.start()].strip()
                return answer, sentiment_data
            except Exception:
                pass
        return text, {"sentiment": "中性", "confidence": 0.5}
