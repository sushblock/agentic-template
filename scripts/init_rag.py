#!/usr/bin/env python3
"""
Initialize the RAG system with sample data
Run this script to populate ChromaDB with sample documents
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rag.ingest import ingest_sample_data
from ops.observability.logging import setup_logging
from ops.config.settings import settings


def main():
    """Initialize RAG system with sample data"""
    print("🚀 Initializing RAG system with ChromaDB...")
    
    # Setup logging
    setup_logging(settings.log_level)
    
    try:
        # Ingest sample business documents
        ingest_sample_data()
        
        print("✅ RAG system initialized successfully!")
        print(f"📁 ChromaDB data stored in: {settings.chroma_persist_directory}")
        print(f"📚 Collection name: {settings.chroma_collection_name}")
        print("\n🎯 You can now test the agent with RAG-enabled queries!")
        
    except Exception as e:
        print(f"❌ Error initializing RAG system: {e}")
        print("\n💡 Make sure you have:")
        print("   - OPENAI_API_KEY set in your .env file")
        print("   - Required dependencies installed: pip install -r requirements.txt")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
