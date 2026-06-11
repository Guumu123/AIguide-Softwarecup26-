import asyncio
import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_services import tts_service, llm_service, rag_service
from app.services.emotion_service import emotion_service

router = APIRouter()

@router.post('/', response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 1. RAG检索
    context_docs = rag_service.retrieve(request.message, k=3)

    # 2. LLM: 导游问答 + 文本情感分析
    llm_response = llm_service.chat_with_sentiment(request.message, context=context_docs)
    answer = llm_response['answer']
    text_emo = llm_response['sentiment']
    confidence = llm_response['confidence']

    # 3. 情感融合 (纯文本模式下，语音情感默认为中性)
    final_emotion_data = emotion_service.get_fused_emotion('neutral', text_emo, confidence)

    # 4. QwenTTS语音合成
    audio_url = tts_service.synthesize(answer, emotion=final_emotion_data['emotion'])

    return {
        'text': answer,
        'audio_url': audio_url,
        'emotion': final_emotion_data['emotion'],
        'intensity': final_emotion_data['intensity'],
        'debug': final_emotion_data['sources']
    }


@router.post('/stream')
async def chat_stream(request: ChatRequest):
    """SSE 流式输出 - 提升交互体验，逐字返回回答内容"""

    async def event_generator():
        # 1. RAG检索
        context_docs = rag_service.retrieve(request.message, k=3)
        yield f"data: {json.dumps({'type': 'searching', 'context_count': len(context_docs)}, ensure_ascii=False)}\n\n"

        # 2. LLM问答
        llm_response = llm_service.chat_with_sentiment(request.message, context=context_docs)
        answer = llm_response['answer']
        text_emo = llm_response['sentiment']
        confidence = llm_response['confidence']

        # 3. 逐字流式输出文本
        for i in range(0, len(answer), 3):
            chunk = answer[i:i+3]
            yield f"data: {json.dumps({'type': 'text', 'content': chunk}, ensure_ascii=False)}\n\n"
            await asyncio.sleep(0.03)

        # 4. 情感融合
        final_emotion_data = emotion_service.get_fused_emotion('neutral', text_emo, confidence)
        yield f"data: {json.dumps({'type': 'emotion', 'emotion': final_emotion_data['emotion'], 'intensity': final_emotion_data['intensity']}, ensure_ascii=False)}\n\n"

        # 5. TTS音频URL
        audio_url = tts_service.synthesize(answer, emotion=final_emotion_data['emotion'])
        yield f"data: {json.dumps({'type': 'audio', 'url': audio_url, 'emotion': final_emotion_data['emotion'], 'intensity': final_emotion_data['intensity']}, ensure_ascii=False)}\n\n"

        # 6. 结束信号
        yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
