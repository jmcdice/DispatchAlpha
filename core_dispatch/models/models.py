from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    Boolean,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    transcription = Column(Text)
    response = Column(Text)
    persona = Column(String)
    scenario = Column(String)
    audio_file = Column(String)
    meta_data = Column(JSON)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    event_type = Column(String, index=True)
    details = Column(JSON)


class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    scenario_type = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    is_active = Column(Boolean, default=True)
    version = Column(Integer, default=1)
    parent_id = Column(Integer, ForeignKey("personas.id"), nullable=True)
    config_json = Column(JSON)

    versions = relationship("PersonaVersion", back_populates="persona")


class PersonaVersion(Base):
    __tablename__ = "persona_versions"

    id = Column(Integer, primary_key=True, index=True)
    persona_id = Column(Integer, ForeignKey("personas.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    config_json = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String)
    change_notes = Column(Text)

    persona = relationship("Persona", back_populates="versions")


class PersonaTemplate(Base):
    __tablename__ = "persona_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    base_config = Column(JSON)
    category = Column(String, index=True)
