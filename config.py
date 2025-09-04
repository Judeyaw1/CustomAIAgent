"""
Configuration settings for the RAG system
"""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class RAGConfig:
    # Model settings
    llm_model: str = "llama3.2:3b"  # Fast model for better performance
    embedding_model: str = "nomic-embed-text"  # Faster embedding model
    
    # Database settings
    chroma_path: str = "chroma"
    data_path: str = "Data"
    
    # Chunking settings
    chunk_size: int = 1000  # Increased from 400
    chunk_overlap: int = 200  # Increased from 100
    
    # Retrieval settings
    top_k: int = 3  # Reduced for faster processing
    similarity_threshold: float = 0.6  # Lowered for more results
    
    # Performance settings
    batch_size: int = 10
    max_retries: int = 3
    
    # UI settings
    show_sources: bool = True
    show_scores: bool = False
    
    @classmethod
    def from_env(cls) -> 'RAGConfig':
        """Load configuration from environment variables"""
        return cls(
            llm_model=os.getenv("LLM_MODEL", cls.llm_model),
            embedding_model=os.getenv("EMBEDDING_MODEL", cls.embedding_model),
            chroma_path=os.getenv("CHROMA_PATH", cls.chroma_path),
            data_path=os.getenv("DATA_PATH", cls.data_path),
            chunk_size=int(os.getenv("CHUNK_SIZE", cls.chunk_size)),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", cls.chunk_overlap)),
            top_k=int(os.getenv("TOP_K", cls.top_k)),
            similarity_threshold=float(os.getenv("SIMILARITY_THRESHOLD", cls.similarity_threshold)),
        )

# Global configuration instance
config = RAGConfig.from_env()
