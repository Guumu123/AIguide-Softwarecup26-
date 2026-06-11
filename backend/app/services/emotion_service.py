from typing import Dict

def fuse_emotion(voice_emotion: str, text_sentiment: str, text_confidence: float) -> Dict:
    """
    情感融合核心逻辑:
    融合规则: 文本为主（70%权重），语音为辅（30%权重）
    """
    emotion_map = {
        'happy': 'happy', 
        'sad': 'sad', 
        'angry': 'angry',
        'neutral': 'neutral',
        '积极': 'happy', 
        '消极': 'sad', 
        '中性': 'neutral'
    }
    
    v = emotion_map.get(voice_emotion, 'neutral')
    t = emotion_map.get(text_sentiment, 'neutral')

    # 融合规则:
    # 1. 语音愤怒优先，转为悲伤(安抚)
    if v == 'angry':
        final = 'sad'
        intensity = 0.9
    # 2. 文本消极，设为悲伤(安慰)
    elif t == 'sad':
        final = 'sad'
        intensity = 0.7
    # 3. 双通道一致积极
    elif v == 'happy' and t == 'happy':
        final = 'happy'
        intensity = 0.95
    # 4. 文本主导积极
    elif t == 'happy':
        final = 'happy'
        intensity = 0.75
    # 5. 默认中性
    else:
        final = 'neutral'
        intensity = 0.5

    return {
        'emotion': final, 
        'intensity': intensity, 
        'sources': {'voice': v, 'text': t}
    }

class EmotionService:
    def get_fused_emotion(self, voice_emo: str, text_emo: str, confidence: float) -> Dict:
        return fuse_emotion(voice_emo, text_emo, confidence)

emotion_service = EmotionService()
