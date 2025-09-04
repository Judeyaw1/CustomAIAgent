"""
Enhanced query system with better error handling and features
"""
import logging
import time
from typing import List, Dict, Any, Optional
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_community.llms.ollama import Ollama
from get_embedding_function import get_embedding_function
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ENHANCED_PROMPT_TEMPLATE = """
You are a helpful AI assistant. Answer the question based on the provided context.

Context:
{context}

Question: {question}

Instructions:
- Provide a clear, accurate answer based on the context
- If the context doesn't contain enough information, say so
- Be concise but comprehensive
- Use bullet points or numbered lists when appropriate
"""

class EnhancedRAGSystem:
    def __init__(self):
        self.embedding_function = get_embedding_function()
        self.db = None
        self.model = None
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize database and model with error handling"""
        try:
            logger.info("Initializing ChromaDB...")
            self.db = Chroma(
                persist_directory=config.chroma_path, 
                embedding_function=self.embedding_function
            )
            logger.info("ChromaDB initialized successfully")
            
            logger.info(f"Initializing LLM model: {config.llm_model}")
            self.model = OllamaLLM(model=config.llm_model)
            logger.info("LLM model initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            raise
    
    def query_with_retry(self, query_text: str, max_retries: int = None) -> Dict[str, Any]:
        """Query with retry logic and comprehensive error handling"""
        max_retries = max_retries or config.max_retries
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Processing query (attempt {attempt + 1}): {query_text[:50]}...")
                start_time = time.time()
                
                result = self._process_query(query_text)
                
                processing_time = time.time() - start_time
                logger.info(f"Query processed successfully in {processing_time:.2f}s")
                
                return {
                    "success": True,
                    "response": result["response"],
                    "sources": result["sources"],
                    "processing_time": processing_time,
                    "attempt": attempt + 1
                }
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    return {
                        "success": False,
                        "error": str(e),
                        "attempts": max_retries
                    }
                time.sleep(1)  # Brief delay before retry
    
    def _process_query(self, query_text: str) -> Dict[str, Any]:
        """Core query processing logic"""
        if not query_text.strip():
            raise ValueError("Query cannot be empty")
        
        # Search the database
        results = self.db.similarity_search_with_score(
            query_text, 
            k=config.top_k
        )
        
        if not results:
            return {
                "response": "I couldn't find any relevant information in the knowledge base.",
                "sources": []
            }
        
        # Filter results by similarity threshold
        filtered_results = [
            (doc, score) for doc, score in results 
            if score >= config.similarity_threshold
        ]
        
        if not filtered_results:
            return {
                "response": "I found some information, but it may not be highly relevant to your question.",
                "sources": [doc.metadata.get("id", "Unknown") for doc, _ in results[:3]]
            }
        
        # Prepare context
        context_text = "\n\n---\n\n".join([
            doc.page_content for doc, _ in filtered_results
        ])
        
        # Generate response
        prompt_template = ChatPromptTemplate.from_template(ENHANCED_PROMPT_TEMPLATE)
        prompt = prompt_template.format(
            context=context_text, 
            question=query_text
        )
        
        response_text = self.model.invoke(prompt)
        
        # Extract sources
        sources = [doc.metadata.get("id", "Unknown") for doc, _ in filtered_results]
        
        return {
            "response": response_text,
            "sources": sources
        }
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            items = self.db.get(include=[])
            return {
                "total_documents": len(items["ids"]),
                "database_path": config.chroma_path
            }
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {"error": str(e)}

# Global instance
rag_system = EnhancedRAGSystem()

def query_rag(query_text: str) -> str:
    """Enhanced query function with better error handling"""
    result = rag_system.query_with_retry(query_text)
    
    if result["success"]:
        response = result["response"]
        sources = result["sources"]
        
        # Format output
        output = f"🤖 Response: {response}\n"
        
        if config.show_sources and sources:
            output += f"\n📚 Sources: {', '.join(sources[:3])}"
        
        if config.show_scores:
            output += f"\n⏱️ Processing time: {result['processing_time']:.2f}s"
        
        print(output)
        return response
    else:
        error_msg = f"❌ Error: {result['error']}"
        print(error_msg)
        return error_msg
