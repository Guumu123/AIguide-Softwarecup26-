from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey, Text, Boolean, Date
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.session import Base

class AvatarPreset(Base):
    __tablename__ = "avatar_presets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    costume_theme = Column(String(20))
    voice_type = Column(String(20))
    ui_theme = Column(String(20))
    speech_style = Column(String(20))
    voice_speed = Column(Float, default=1.0)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TouristBehavior(Base):
    __tablename__ = "tourist_behaviors"
    id = Column(Integer, primary_key=True, index=True)
    tourist_id = Column(String(20))
    user_nickname = Column(String(100))
    age = Column(Integer)
    gender = Column(String(10))
    attraction_name = Column(String(100))
    attraction_type = Column(String(50))
    visit_date = Column(Date)
    stay_duration = Column(Float)
    ticket_cost = Column(Float)
    food_cost = Column(Float)
    shopping_cost = Column(Float)
    transport_cost = Column(Float)
    entertainment_cost = Column(Float)
    total_cost = Column(Float)
    group_size = Column(Integer)
    satisfaction = Column(Integer)
    imported_at = Column(DateTime(timezone=True), server_default=func.now())

class KBDocument(Base):
    __tablename__ = "kb_documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(Text, nullable=False)
    doc_type = Column(String(50))
    source_file = Column(String(200))
    chunk_index = Column(Integer)
    embedding_model = Column(String(50))
    metadata = Column(JSONB)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
