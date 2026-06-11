from fastapi import APIRouter, UploadFile, File, Depends
from app.schemas.chat import VoiceResponse
from app.services.ai_services import asr_service, tts_service, llm_service, rag_service
from app.services.emotion_service import emotion_service
import aiofiles
import os
import uuid

router = APIRouter()

@router.post('/upload', response_model=VoiceResponse)
async def handle_voice(file: UploadFile = File(...)):
    # 1. 保存音频 (使用 UUID 避免中文字符或重名问题)
    file_ext = os.path.splitext(file.filename)[1]
    temp_filename = f"{uuid.uuid4()}{file_ext}"
    temp_path = os.path.join("/tmp" if os.name != 'nt' else ".", temp_filename)
    
    async with aiofiles.open(temp_path, "wb") as buffer:
        content = await file.read()
        await buffer.write(content)

    try:
        # 2. FunASR: 语音识别 + 语音情感
        asr_result = asr_service.transcribe(temp_path)
        text = asr_result['text']
        voice_emo = asr_result.get('emotion', 'neutral')

        # 3. RAG检索
        context_docs = rag_service.retrieve(text, k=3)

        # 4. LLM: 导游问答 + 文本情感分析
        llm_response = llm_service.chat_with_sentiment(text, context=context_docs)
        answer = llm_response['answer']
        text_emo = llm_response['sentiment']
        confidence = llm_response['confidence']

        # 5. 双通道情感融合
        final_emotion_data = emotion_service.get_fused_emotion(voice_emo, text_emo, confidence)

        # 6. QwenTTS语音合成
        audio_url = tts_service.synthesize(answer, emotion=final_emotion_data['emotion'])

        return {
            'text': answer,
            'audio_url': audio_url,
            'emotion': final_emotion_data['emotion'],
            'intensity': final_emotion_data['intensity'],
            'debug': final_emotion_data['sources']
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
