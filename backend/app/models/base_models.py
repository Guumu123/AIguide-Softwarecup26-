from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey, Text, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(64), unique=True, nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    group_size = Column(Integer, default=1)
    interests = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    message_type = Column(String(10))
    sentiment = Column(String(10))
    sentiment_intensity = Column(Float)
    voice_sentiment = Column(String(10))
    text_sentiment = Column(String(10))
    text_confidence = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Attraction(Base):
    __tablename__ = "attractions"
    id = Column(Integer, primary_key=True, index=True)
    attraction_id = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    scenic_area = Column(String(50))
    location = Column(Text)
    parameters = Column(Text)
    core_function = Column(Text)
    cultural_meaning = Column(Text)
    detailed_intro = Column(Text)
    highlights = Column(Text)
    performance_info = Column(Text)
    notes = Column(Text)
    estimated_duration = Column(Float)
    category = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class FAQ(Base):
    __tablename__ = "faq"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(50))
    hit_count = Column(Integer, default=0)
    is_hot = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class RouteRecommendation(Base):
    __tablename__ = "route_recommendations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    route_json = Column(JSONB, nullable=False)
    total_duration = Column(Float)
    estimated_cost = Column(JSONB)
    speech_highlights = Column(JSONB)
    user_feedback = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
