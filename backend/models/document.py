from sqlalchemy import Column, Integer, String, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from backend.core.db import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_type = Column(String) # 'plan' or 'spec'
    metadata_json = Column(JSON, default={})
    
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    page_number = Column(Integer)
    section = Column(String, nullable=True) # E.g., "09 29 00 Gypsum Board"
    content = Column(Text)
    content_type = Column(String) # 'text' or 'table'
    embedding = Column(Vector(1536)) # Dimension depends on embedding model
    
    document = relationship("Document", back_populates="chunks")
