"""
Enhanced main application with better UX and error handling
"""
import os
import sys
import logging
from typing import Optional
from enhanced_query import rag_system, query_rag
from config import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RAGApplication:
    def __init__(self):
        self.conversation_history = []
        self.running = True
    
    def print_welcome(self):
        """Print welcome message and system info"""
        print("=" * 60)
        print("🤖 Enhanced RAG System")
        print("=" * 60)
        
        # Get database stats
        stats = rag_system.get_database_stats()
        if "error" not in stats:
            print(f"📊 Database: {stats['total_documents']} documents loaded")
        else:
            print(f"⚠️  Database: {stats['error']}")
        
        print(f"🧠 Model: {config.llm_model}")
        print(f"🔍 Embedding: {config.embedding_model}")
        print("=" * 60)
        print("💡 Type 'help' for commands, 'quit' to exit")
        print("=" * 60)
    
    def print_help(self):
        """Print help information"""
        print("\n📖 Available Commands:")
        print("  help     - Show this help message")
        print("  stats    - Show database statistics")
        print("  clear    - Clear conversation history")
        print("  quit/exit - Exit the application")
        print("\n💬 Just type your question to get started!")
    
    def handle_command(self, user_input: str) -> bool:
        """Handle special commands. Returns True if command was handled."""
        command = user_input.lower().strip()
        
        if command in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            return True
        
        elif command == 'help':
            self.print_help()
            return True
        
        elif command == 'stats':
            stats = rag_system.get_database_stats()
            if "error" not in stats:
                print(f"\n📊 Database Statistics:")
                print(f"  Documents: {stats['total_documents']}")
                print(f"  Path: {stats['database_path']}")
            else:
                print(f"❌ Error getting stats: {stats['error']}")
            return True
        
        elif command == 'clear':
            self.conversation_history = []
            print("🧹 Conversation history cleared!")
            return True
        
        return False
    
    def get_user_input(self, prompt: str = "❓ Your question: ") -> Optional[str]:
        """Get user input with better error handling"""
        try:
            user_input = input(prompt).strip()
            return user_input if user_input else None
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return None
        except EOFError:
            print("\n👋 Goodbye!")
            return None
    
    def process_query(self, query: str):
        """Process a user query"""
        if not query:
            print("⚠️  Please enter a valid question.")
            return
        
        # Add to conversation history
        self.conversation_history.append({"type": "user", "content": query})
        
        try:
            # Process the query
            response = query_rag(query)
            
            # Add response to history
            self.conversation_history.append({"type": "assistant", "content": response})
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            print(f"❌ Sorry, I encountered an error: {e}")
    
    def run(self):
        """Main application loop"""
        self.print_welcome()
        
        while self.running:
            try:
                # Get user input
                user_input = self.get_user_input()
                
                if user_input is None:  # User wants to quit
                    break
                
                # Handle special commands
                if self.handle_command(user_input):
                    if user_input.lower().strip() in ['quit', 'exit', 'q']:
                        break
                    continue
                
                # Process regular query
                self.process_query(user_input)
                
                # Ask if user wants to continue
                print("\n" + "-" * 40)
                continue_input = self.get_user_input("🔄 Another question? (y/n): ")
                
                if continue_input and continue_input.lower().startswith('n'):
                    print("👋 Goodbye!")
                    break
                
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}")
                print(f"❌ An unexpected error occurred: {e}")
                print("🔄 Please try again or type 'quit' to exit.")

def main():
    """Main entry point"""
    try:
        app = RAGApplication()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
