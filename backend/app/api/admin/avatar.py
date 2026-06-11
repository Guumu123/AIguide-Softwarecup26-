from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_current_admin
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

_presets = [
    {
        "id": 1, "name": "禅意主题", "costume_theme": "zen", "voice_type": "warm_female",
        "ui_theme": "zen_cyan", "speech_style": "academic", "voice_speed": 1.0,
        "is_default": True
    },
    {
        "id": 2, "name": "佛教主题", "costume_theme": "buddhist", "voice_type": "calm_male",
        "ui_theme": "buddhist_gold", "speech_style": "story", "voice_speed": 0.9,
        "is_default": False
    },
    {
        "id": 3, "name": "现代主题", "costume_theme": "modern", "voice_type": "warm_female",
        "ui_theme": "nature_green", "speech_style": "family", "voice_speed": 1.1,
        "is_default": False
    },
]
_next_id = 4


class PresetCreate(BaseModel):
    name: str
    costume_theme: str = "zen"
    voice_type: str = "warm_female"
    ui_theme: str = "zen_cyan"
    speech_style: str = "academic"
    voice_speed: float = 1.0
    is_default: bool = False


class PresetUpdate(BaseModel):
    name: Optional[str] = None
    costume_theme: Optional[str] = None
    voice_type: Optional[str] = None
    ui_theme: Optional[str] = None
    speech_style: Optional[str] = None
    voice_speed: Optional[float] = None
    is_default: Optional[bool] = None


@router.get('/presets', dependencies=[Depends(get_current_admin)])
async def list_presets():
    return {"total": len(_presets), "items": _presets}


@router.post('/presets', dependencies=[Depends(get_current_admin)])
async def create_preset(data: PresetCreate):
    global _next_id
    item = data.model_dump()
    item["id"] = _next_id
    _next_id += 1
    _presets.append(item)
    return item


@router.put('/presets/{preset_id}', dependencies=[Depends(get_current_admin)])
async def update_preset(preset_id: int, data: PresetUpdate):
    for p in _presets:
        if p["id"] == preset_id:
            updates = data.model_dump(exclude_none=True)
            p.update(updates)
            return p
    raise HTTPException(status_code=404, detail="形象方案不存在")


@router.delete('/presets/{preset_id}', dependencies=[Depends(get_current_admin)])
async def delete_preset(preset_id: int):
    global _presets
    _presets = [p for p in _presets if p["id"] != preset_id]
    return {"status": "deleted"}
