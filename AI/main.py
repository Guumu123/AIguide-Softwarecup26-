# main.py

import asyncio
import os
from src.services.llm_service import LLMService
from src.services.rag_service import RAGService, BGEM3Embedder, ChromaDBStore
from src.services.tts_service import TTSService

async def main():
    # 1. 初始化服务
    # 实际使用时请设置环境变量 DASHSCOPE_API_KEY
    api_key = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")
    
    llm = LLMService(api_key=api_key)
    tts = TTSService(api_key=api_key)
    
    # 初始化 RAG 服务 (使用 Mock 嵌入和向量库)
    embedder = BGEM3Embedder()
    vector_store = ChromaDBStore()
    rag = RAGService(embedder=embedder, vector_store=vector_store)

    print("=== AI 景区向导系统初始化完成 ===\n")

    # 2. 模拟添加知识库文档
    print("正在构建知识库...")
    await rag.add_document(
        content="灵山大佛通高88米，主体79米，莲花瓣9米。含台基总高101.5米。",
        metadata={"attraction_name": "灵山大佛", "type": "事实性"}
    )
    print("知识库构建完成。\n")

    # 3. 模拟游客提问
    question = "灵山大佛有多高？"
    print(f"游客提问: {question}")

    # 4. RAG 检索
    context = await rag.retrieve(question)
    context_text = "\n".join(context)
    print(f"检索到的上下文: {context_text}")

    # 5. LLM 生成回答
    print("AI 正在思考...")
    # 注意：如果没有真实的 API Key，这里会返回错误或 Mock 数据
    result = await llm.chat_with_sentiment(question, context=context_text)
    
    print(f"AI 回答: {result['answer']}")
    print(f"识别情感: {result['sentiment']} (置信度: {result['confidence']})")

    # 6. TTS 语音合成
    if result['answer']:
        print("\n正在生成语音...")
        audio_path = await tts.synthesize(result['answer'], emotion=result['sentiment'])
        if audio_path:
            print(f"语音已生成: {audio_path}")
        else:
            print("语音生成失败（可能缺少 API Key）")

    # 7. 模拟路线生成
    print("\n=== 模拟路线生成 ===")
    user_profile = {
        "age": 25,
        "gender": "女",
        "group_size": 2,
        "interests": "历史, 摄影"
    }
    route = await llm.generate_route(user_profile)
    print(f"生成的推荐路线: {route}")

if __name__ == "__main__":
    asyncio.run(main())
