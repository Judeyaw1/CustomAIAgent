"""
Enhanced database population with better error handling and progress tracking
"""
import argparse
import os
import shutil
import logging
from typing import List, Optional
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
from langchain_chroma import Chroma
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedDatabasePopulator:
    def __init__(self):
        self.embedding_function = get_embedding_function()
        self.db = None
    
    def initialize_database(self):
        """Initialize the ChromaDB connection"""
        try:
            logger.info(f"Initializing database at: {config.chroma_path}")
            self.db = Chroma(
                persist_directory=config.chroma_path,
                embedding_function=self.embedding_function
            )
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def load_documents(self) -> List[Document]:
        """Load documents from the data directory"""
        if not os.path.exists(config.data_path):
            raise FileNotFoundError(f"Data directory not found: {config.data_path}")
        
        logger.info(f"Loading documents from: {config.data_path}")
        
        try:
            document_loader = PyPDFDirectoryLoader(config.data_path)
            documents = document_loader.load()
            
            logger.info(f"Loaded {len(documents)} documents")
            return documents
            
        except Exception as e:
            logger.error(f"Failed to load documents: {e}")
            raise
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks with enhanced settings"""
        logger.info(f"Splitting documents with chunk_size={config.chunk_size}, overlap={config.chunk_overlap}")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=len,
            is_separator_regex=False,
            separators=["\n\n", "\n", " ", ""]  # Better separators
        )
        
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")
        
        return chunks
    
    def calculate_chunk_ids(self, chunks: List[Document]) -> List[Document]:
        """Calculate unique IDs for chunks with better metadata"""
        logger.info("Calculating chunk IDs...")
        
        last_page_id = None
        current_chunk_index = 0
        
        for chunk in chunks:
            source = chunk.metadata.get("source", "unknown")
            page = chunk.metadata.get("page", 0)
            current_page_id = f"{source}:{page}"
            
            # If the page ID is the same as the last one, increment the index
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0
            
            # Calculate the chunk ID
            chunk_id = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id
            
            # Enhanced metadata
            chunk.metadata.update({
                "id": chunk_id,
                "chunk_index": current_chunk_index,
                "page_id": current_page_id,
                "chunk_size": len(chunk.page_content)
            })
        
        logger.info("Chunk IDs calculated successfully")
        return chunks
    
    def add_to_database(self, chunks: List[Document]) -> dict:
        """Add chunks to database with progress tracking"""
        if not self.db:
            raise RuntimeError("Database not initialized")
        
        # Calculate chunk IDs
        chunks_with_ids = self.calculate_chunk_ids(chunks)
        
        # Get existing items
        try:
            existing_items = self.db.get(include=[])
            existing_ids = set(existing_items["ids"])
            logger.info(f"Found {len(existing_ids)} existing documents in database")
        except Exception as e:
            logger.warning(f"Could not retrieve existing items: {e}")
            existing_ids = set()
        
        # Filter new chunks
        new_chunks = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)
        
        result = {
            "total_chunks": len(chunks_with_ids),
            "existing_chunks": len(existing_ids),
            "new_chunks": len(new_chunks),
            "added": False
        }
        
        if new_chunks:
            logger.info(f"Adding {len(new_chunks)} new chunks to database...")
            
            try:
                # Add in batches for better performance
                batch_size = config.batch_size
                for i in range(0, len(new_chunks), batch_size):
                    batch = new_chunks[i:i + batch_size]
                    batch_ids = [chunk.metadata["id"] for chunk in batch]
                    
                    logger.info(f"Adding batch {i//batch_size + 1}/{(len(new_chunks)-1)//batch_size + 1}")
                    self.db.add_documents(batch, ids=batch_ids)
                
                result["added"] = True
                logger.info("✅ New chunks added successfully")
                
            except Exception as e:
                logger.error(f"Failed to add chunks: {e}")
                raise
        else:
            logger.info("✅ No new chunks to add")
        
        return result
    
    def clear_database(self):
        """Clear the database"""
        if os.path.exists(config.chroma_path):
            logger.info("Clearing database...")
            shutil.rmtree(config.chroma_path)
            logger.info("✅ Database cleared")
        else:
            logger.info("Database doesn't exist, nothing to clear")
    
    def get_database_stats(self) -> dict:
        """Get database statistics"""
        if not self.db:
            return {"error": "Database not initialized"}
        
        try:
            items = self.db.get(include=[])
            return {
                "total_documents": len(items["ids"]),
                "database_path": config.chroma_path
            }
        except Exception as e:
            return {"error": str(e)}
    
    def populate(self, reset: bool = False) -> dict:
        """Main population method"""
        try:
            if reset:
                self.clear_database()
            
            self.initialize_database()
            
            # Load and process documents
            documents = self.load_documents()
            chunks = self.split_documents(documents)
            
            # Add to database
            result = self.add_to_database(chunks)
            
            # Get final stats
            stats = self.get_database_stats()
            result.update(stats)
            
            return result
            
        except Exception as e:
            logger.error(f"Population failed: {e}")
            raise

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Enhanced RAG Database Population")
    parser.add_argument("--reset", action="store_true", help="Reset the database before populating")
    parser.add_argument("--stats", action="store_true", help="Show database statistics only")
    args = parser.parse_args()
    
    populator = EnhancedDatabasePopulator()
    
    try:
        if args.stats:
            populator.initialize_database()
            stats = populator.get_database_stats()
            print(f"📊 Database Statistics:")
            print(f"  Documents: {stats.get('total_documents', 'Unknown')}")
            print(f"  Path: {stats.get('database_path', 'Unknown')}")
        else:
            print("🚀 Starting database population...")
            result = populator.populate(reset=args.reset)
            
            print(f"\n✅ Population completed!")
            print(f"📊 Results:")
            print(f"  Total chunks: {result['total_chunks']}")
            print(f"  Existing chunks: {result['existing_chunks']}")
            print(f"  New chunks: {result['new_chunks']}")
            print(f"  Added: {'Yes' if result['added'] else 'No'}")
            print(f"  Final document count: {result['total_documents']}")
            
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
