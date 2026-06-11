# src/services/rag_service.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
import asyncio

class RAGService:
    def __init__(self, embedder=None, vector_store=None):
        self.embedder = embedder # Should be an instance of BGEM3Embedder
        self.vector_store = vector_store # Should be an instance of ChromaDBStore
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800, chunk_overlap=100,
            separators=['\n\n', '\n', '。', '；', '，', ' ', '']
        )

    async def retrieve(self, query, k=3):
        if not self.embedder or not self.vector_store:
            return ["知识库未初始化"]
            
        query_embedding = await self.embedder.embed(query)
        results = await self.vector_store.similarity_search(
            embedding=query_embedding,
            k=k,
            filter={"is_active": True}
        )
        
        if len(results) > 1:
            results = await self._rerank(query, results)
            
        return [r["content"] for r in results]

    async def add_document(self, content, metadata):
        if not self.embedder or not self.vector_store:
            return
            
        chunks = self.text_splitter.split_text(content)
        for i, chunk in enumerate(chunks):
            embedding = await self.embedder.embed(chunk)
            chunk_metadata = {
                **metadata,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            await self.vector_store.add(
                embedding=embedding,
                document=chunk,
                metadata=chunk_metadata
            )

    async def _rerank(self, query, results):
        scored = []
        for r in results:
            score = await self.embedder.similarity(query, r["content"])
            scored.append((score, r))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [r for _, r in scored]

# Placeholder classes for demonstration
class BGEM3Embedder:
    async def embed(self, text):
        # In a real implementation, this would call the BGE-M3 model
        return [0.0] * 1024

    async def similarity(self, query, text):
        return 0.5

class ChromaDBStore:
    def __init__(self):
        self.data = []

    async def similarity_search(self, embedding, k=3, filter=None):
        return self.data[:k]

    async def add(self, embedding, document, metadata):
        self.data.append({"embedding": embedding, "content": document, "metadata": metadata})
