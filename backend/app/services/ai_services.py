"""AI 服务层 - LLM / TTS / ASR / RAG"""
import os
import uuid
import httpx
import random
from pathlib import Path
from app.config import settings


class ASRService:
    """语音识别服务 - 支持 FunASR 本地部署和 Mock 降级"""

    FUNASR_SERVER_URL = os.getenv("FUNASR_SERVER_URL", "http://localhost:8089")

    async def transcribe(self, file_path: str) -> dict:
        """
        调用 FunASR 语音识别 + 情感分析
        需要部署 FunASR SenseVoice-Small 服务后才能使用 HTTP 模式
        """
        # 尝试调用本地 FunASR 服务
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                with open(file_path, "rb") as f:
                    response = await client.post(
                        f"{self.FUNASR_SERVER_URL}/asr",
                        files={"file": f},
                    )
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "text": data.get("text", ""),
                        "emotion": data.get("emotion", "neutral"),
                        "confidence": data.get("confidence", 0.8),
                    }
        except Exception:
            pass  # 降级到 Mock

        # Mock 降级
        texts = [
            "你好，请问灵山大佛怎么走？",
            "九龙灌浴表演时间是什么时候？",
            "梵宫的建筑风格太震撼了！",
            "附近有什么好吃的素斋吗？",
            "这里的历史文化好深厚啊。",
        ]
        emotions = ["neutral", "neutral", "happy", "neutral", "happy"]
        idx = random.randint(0, len(texts) - 1)
        return {
            "text": texts[idx],
            "emotion": emotions[idx],
            "confidence": 0.85,
        }


class TTSService:
    """语音合成服务 - 支持 QwenTTS 云端和本地降级"""

    TTS_CACHE_DIR = Path("data/tts_cache")
    QWEN_TTS_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-to-speech"

    def __init__(self):
        self.TTS_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    async def synthesize(self, text: str, emotion: str = "neutral") -> str:
        """
        调用 QwenTTS 语音合成
        emotion: happy / sad / neutral / surprised / confused
        """
        api_key = settings.DASHSCOPE_API_KEY
        if api_key and api_key != "your-api-key-here":
            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    response = await client.post(
                        self.QWEN_TTS_URL,
                        headers={"Authorization": f"Bearer {api_key}"},
                        json={
                            "model": "qwen-tts",
                            "input": {"text": text},
                            "parameters": {
                                "voice": self._emotion_to_voice(emotion),
                                "speech_rate": self._emotion_to_speed(emotion),
                            },
                        },
                    )
                    if response.status_code == 200:
                        data = response.json()
                        if "output" in data and "audio_url" in data["output"]:
                            return data["output"]["audio_url"]
            except Exception:
                pass

        # Mock 降级
        return f"/api/audio/tts_{uuid.uuid4().hex[:8]}.mp3"

    @staticmethod
    def _emotion_to_voice(emotion: str) -> str:
        mapping = {
            "happy": "Cherry", "sad": "Stella", "surprised": "Lydia",
            "confused": "Stella", "neutral": "Cherry",
        }
        return mapping.get(emotion, "Cherry")

    @staticmethod
    def _emotion_to_speed(emotion: str) -> float:
        mapping = {"happy": 1.1, "sad": 0.85, "surprised": 1.15, "confused": 0.9, "neutral": 1.0}
        return mapping.get(emotion, 1.0)


class LLMService:
    """大语言模型服务 - Qwen2.5 via DashScope"""

    DASHSCOPE_CHAT_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    MODEL = "qwen2.5-14b-instruct"

    async def chat_with_sentiment(self, text: str, context: list = None) -> dict:
        api_key = settings.DASHSCOPE_API_KEY
        if api_key and api_key != "your-api-key-here":
            try:
                messages = [{"role": "system", "content": self._build_system_prompt()}]
                if context:
                    ctx_str = "\n".join(f"- {doc}" for doc in context)
                    messages.append({"role": "system", "content": f"参考知识库：\n{ctx_str}"})
                messages.append({"role": "user", "content": text})

                async with httpx.AsyncClient(timeout=60) as client:
                    response = await client.post(
                        self.DASHSCOPE_CHAT_URL,
                        headers={"Authorization": f"Bearer {api_key}"},
                        json={"model": self.MODEL, "messages": messages, "temperature": 0.7},
                    )
                    if response.status_code == 200:
                        data = response.json()
                        answer = data["choices"][0]["message"]["content"]
                        sentiment, confidence = self._parse_sentiment(answer)
                        return {"answer": answer, "sentiment": sentiment, "confidence": confidence}
            except Exception:
                pass

        # Mock 降级
        return self._mock_chat(text, context)

    def _build_system_prompt(self) -> str:
        return (
            "你是一个专业的景区导游AI数字人，服务于灵山胜境和拈花湾景区。\n"
            "要求：\n"
            "1. 使用亲切热情的语气回答游客问题\n"
            "2. 基于知识库提供准确信息，不编造\n"
            "3. 回答尽量简洁，不超过150字\n"
            "4. 如果问题超出知识范围，礼貌引导游客咨询人工服务\n"
            "5. 在回答末尾标注情感标签：[情感:积极/中性/消极]"
        )

    def _parse_sentiment(self, text: str) -> tuple:
        import re
        match = re.search(r'\[情感:\s*(积极|中性|消极)\]', text)
        if match:
            sentiment = match.group(1)
            return sentiment, 0.9
        return "中性", 0.7

    def _mock_chat(self, text: str, context: list = None) -> dict:
        answers = {
            "大佛": "灵山大佛通高88米，佛体79米，莲花瓣9米，总高101.5米，是我国最高的青铜立佛。[情感:积极]",
            "九龙": "九龙灌浴每天上午10:00和下午15:00各有一场表演，建议提前10分钟到场。[情感:中性]",
            "梵宫": "灵山梵宫建筑群气势恢弘，内部有琉璃、木雕等艺术珍品，是必看景点。[情感:积极]",
            "素斋": "景区设有灵山蔬食馆，提供纯素自助餐，人均约68元，位于九龙灌浴东侧。[情感:中性]",
            "门票": "成人票210元，学生及60岁以上老人半价105元，1.2米以下儿童免票。[情感:中性]",
            "轮椅": "景区入口处提供轮椅和婴儿车租赁服务，轮椅押金200元。[情感:中性]",
        }
        for key, answer in answers.items():
            if key in text:
                sentiment, confidence = self._parse_sentiment(answer)
                return {"answer": answer, "sentiment": sentiment, "confidence": confidence}
        return {
            "answer": f"您好！关于'{text[:20]}...'的问题，建议您咨询游客中心或查看景区导览图。[情感:中性]",
            "sentiment": "中性",
            "confidence": 0.7,
        }


class RAGService:
    """RAG 知识库检索服务 - BGE-M3 + ChromaDB"""

    def __init__(self):
        self._kb_loaded = False
        self._docs: list[str] = []

    def _load_knowledge_base(self):
        """加载内置景区知识库"""
        self._docs = [
            "灵山大佛通高88米，佛体79米，莲花瓣9米，含台基总高101.5米，采用锡青铜铸造，是我国最高的青铜立佛。",
            "九龙灌浴表演每日上午10:00和下午15:00各一场，每场约20分钟，展示佛祖诞生九龙吐水场景。",
            "灵山梵宫建筑面积7.2万平方米，融合了佛教文化与现代建筑艺术，内部有大型琉璃壁画和木雕艺术。",
            "五印坛城是藏传佛教建筑风格的景点，供奉五方佛，象征佛的五种智慧，坛城内部有转经筒和佛像。",
            "祥符禅寺始建于唐代，历代多次重修，寺内有天王殿、大雄宝殿、藏经楼，是灵山胜境的发源地。",
            "百子戏弥勒雕塑长13.8米，由青铜铸造而成，弥勒佛斜倚而卧，百名童子在其身上嬉戏玩耍。",
            "灵山蔬食馆提供纯素自助餐，人均约68元，以佛教素斋文化为主，食材新鲜应季。",
            "灵山胜境成人票210元，学生及60岁以上老人半价105元，1.2米以下儿童及70岁以上老人免票。",
            "景区开放时间：夏季(4-10月)7:00-17:30，冬季(11-3月)7:30-17:00。",
            "拈花湾以禅意生活为主题，有梵天花海、五灯湖、鹿鸣谷、一笑堂等景点，适合慢生活体验。",
            "景区内设有免费接驳车，循环发车，间隔约15分钟，沿途经过主要景点。",
            "景区游客中心提供行李寄存、轮椅租赁、婴儿车租赁、医疗急救等服务。",
            "梵宫内有《降魔成道》大型壁画，长48米，高9米，由多位知名画家历时3年创作完成。",
            "灵山大佛基座内部有佛教文化博物馆，展示佛教历史与造像艺术，可乘电梯登临佛脚。",
            "阿育王柱高16.4米，柱身有七宝装饰，柱头蹲踞一对石狮，象征佛法弘扬。",
            "梵宫琉璃壁画《金色华藏》面积达500平方米，由琉璃艺术家制作，展现华藏世界的瑰丽景象。",
            "天下第一掌为灵山大佛右手1:1复制品，高11.7米，宽5.5米，游客可亲手触摸祈福。",
            "景区东侧有古银杏树群，树龄超过800年，每逢深秋金黄一片，是著名的拍照打卡地。",
            "灵山盛境的核心文化是\"灵山一会，俨然未散\"的佛教禅宗精神。",
            "景区周边可品尝太湖三白(白鱼、白虾、银鱼)、无锡排骨、太湖莼菜等地方特色美食。",
        ]
        self._kb_loaded = True

    def retrieve(self, text: str, k: int = 3) -> list:
        """基于关键词的语义检索（Mock BGE-M3 + ChromaDB）"""
        if not self._kb_loaded:
            self._load_knowledge_base()

        keywords = self._extract_keywords(text)
        scored = []
        for doc in self._docs:
            score = sum(1 for kw in keywords if kw in doc)
            if score > 0:
                scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:k]] if scored else [self._docs[0]]

    @staticmethod
    def _extract_keywords(text: str) -> list[str]:
        kw_map = {
            "大佛": ["大佛", "青铜", "高度"], "九龙": ["九龙", "灌浴", "表演"],
            "梵宫": ["梵宫", "壁画", "建筑"], "五印": ["五印", "坛城", "藏传"],
            "门票": ["门票", "票价", "价格"], "素斋": ["素斋", "素食", "用餐"],
            "时间": ["时间", "开放", "关门"], "轮椅": ["轮椅", "租赁"],
            "行李": ["行李", "寄存"], "摆渡": ["摆渡", "接驳"],
            "祥符": ["祥符", "禅寺"], "拈花": ["拈花", "禅意"],
            "灌浴": ["灌浴", "九龙", "表演"], "坛城": ["坛城", "五印", "藏传"],
        }
        keywords = set()
        for query_kw, doc_kws in kw_map.items():
            if query_kw in text:
                keywords.update(doc_kws)
        if not keywords:
            keywords.add(text[:2])
        return list(keywords)


# 全局服务实例
asr_service = ASRService()
tts_service = TTSService()
llm_service = LLMService()
rag_service = RAGService()
