from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.schemas.admin import KBUploadResponse
from app.core.dependencies import get_current_admin
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# --- 内存模拟存储 ---
_documents = [
    {"id": 1, "filename": "灵山文化.docx", "doc_type": "讲解词", "status": "processed", "chunk_count": 24, "update_time": "2024-05-20 10:00:00"},
    {"id": 2, "filename": "景区FAQ.xlsx", "doc_type": "FAQ", "status": "processed", "chunk_count": 56, "update_time": "2024-05-19 15:30:00"},
    {"id": 3, "filename": "梵宫艺术背景.docx", "doc_type": "文史资料", "status": "processing", "chunk_count": 0, "update_time": "2024-05-20 11:15:00"},
]
_faqs = [
    {"id": 1, "question": "灵山大佛有多高？", "answer": "灵山大佛通高88米，佛体79米，莲花瓣9米，含台基总高101.5米。", "category": "景点", "hit_count": 1256, "is_hot": True},
    {"id": 2, "question": "景区门票多少钱？", "answer": "成人票210元，学生及60岁以上老人半价105元，1.2米以下儿童免票。", "category": "门票", "hit_count": 982, "is_hot": True},
    {"id": 3, "question": "九龙灌浴表演时间？", "answer": "每日上午10:00和下午15:00各一场，每场约20分钟。", "category": "景点", "hit_count": 875, "is_hot": True},
]
_next_doc_id = 4
_next_faq_id = 4

# --- KB 文档管理 ---

@router.post('/upload', response_model=KBUploadResponse, dependencies=[Depends(get_current_admin)])
async def upload_kb(file: UploadFile = File(...)):
    global _next_doc_id
    doc_id = _next_doc_id
    _next_doc_id += 1
    _documents.append({
        "id": doc_id, "filename": file.filename, "doc_type": "待分类",
        "status": "processing", "chunk_count": 0, "update_time": "刚刚"
    })
    return {"document_id": doc_id, "status": "processing"}

@router.get('/documents', dependencies=[Depends(get_current_admin)])
async def list_documents():
    return {"total": len(_documents), "items": _documents}

@router.put('/documents/{doc_id}', dependencies=[Depends(get_current_admin)])
async def update_document(doc_id: int, filename: str = None, doc_type: str = None):
    for doc in _documents:
        if doc["id"] == doc_id:
            if filename:
                doc["filename"] = filename
            if doc_type:
                doc["doc_type"] = doc_type
            return doc
    raise HTTPException(status_code=404, detail="文档不存在")

@router.delete('/documents/{doc_id}', dependencies=[Depends(get_current_admin)])
async def delete_document(doc_id: int):
    global _documents
    _documents = [d for d in _documents if d["id"] != doc_id]
    return {"status": "deleted"}

@router.post('/documents/{doc_id}/reindex', dependencies=[Depends(get_current_admin)])
async def reindex_document(doc_id: int):
    """触发 BGE-M3 重新 Embedding"""
    for doc in _documents:
        if doc["id"] == doc_id:
            doc["status"] = "processing"
            return {"doc_id": doc_id, "status": "重新索引已触发", "model": "BGE-M3"}
    raise HTTPException(status_code=404, detail="文档不存在")

# --- FAQ 独立管理 ---

class FAQCreate(BaseModel):
    question: str
    answer: str
    category: Optional[str] = "通用"

class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None
    is_hot: Optional[bool] = None

@router.get('/faq', dependencies=[Depends(get_current_admin)])
async def list_faq(category: str = None, is_hot: bool = None):
    items = _faqs
    if category:
        items = [f for f in items if f["category"] == category]
    if is_hot is not None:
        items = [f for f in items if f["is_hot"] == is_hot]
    return {"total": len(items), "items": items}

@router.post('/faq', dependencies=[Depends(get_current_admin)])
async def create_faq(data: FAQCreate):
    global _next_faq_id
    item = {
        "id": _next_faq_id,
        "question": data.question,
        "answer": data.answer,
        "category": data.category,
        "hit_count": 0,
        "is_hot": False,
    }
    _next_faq_id += 1
    _faqs.append(item)
    return item

@router.put('/faq/{faq_id}', dependencies=[Depends(get_current_admin)])
async def update_faq(faq_id: int, data: FAQUpdate):
    for faq in _faqs:
        if faq["id"] == faq_id:
            if data.question is not None:
                faq["question"] = data.question
            if data.answer is not None:
                faq["answer"] = data.answer
            if data.category is not None:
                faq["category"] = data.category
            if data.is_hot is not None:
                faq["is_hot"] = data.is_hot
            return faq
    raise HTTPException(status_code=404, detail="FAQ不存在")

@router.delete('/faq/{faq_id}', dependencies=[Depends(get_current_admin)])
async def delete_faq(faq_id: int):
    global _faqs
    _faqs = [f for f in _faqs if f["id"] != faq_id]
    return {"status": "deleted"}
