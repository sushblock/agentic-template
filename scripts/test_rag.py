#!/usr/bin/env python3
"""
Test the RAG system integration
Run this script to test ChromaDB retrieval functionality
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rag.retriever import retrieve
from agents.graphs.main_graph import graph
from ops.observability.logging import setup_logging
from ops.config.settings import settings


def test_retrieval():
    """Test basic retrieval functionality"""
    print("🔍 Testing RAG retrieval...")
    
    test_queries = [
        "What are the safety requirements for handling steel materials?",
        "What is the current inventory of steel rods?",
        "What are the quality standards for aluminum sheets?",
        "What is the approval process for purchase orders?",
        "What are the emergency procedures for workplace injuries?"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        result = retrieve(query)
        print(f"📄 Result: {result[:200]}...")
        print("-" * 50)


def test_agent_with_rag():
    """Test the full agent workflow with RAG"""
    print("\n🤖 Testing agent with RAG integration...")
    
    test_goals = [
        "Create a purchase order for 50 steel rods with safety requirements",
        "Check inventory levels for aluminum sheets and create reorder plan",
        "Generate a safety checklist for handling steel materials",
        "Create a quality control report for incoming materials"
    ]
    
    for goal in test_goals:
        print(f"\n🎯 Goal: {goal}")
        try:
            result = graph.invoke({"goal": goal, "approve": False})
            print(f"✅ Plan: {result.get('plan', 'No plan generated')[:100]}...")
            print(f"📄 Draft: {result.get('draft', 'No draft generated')[:200]}...")
            print(f"🔒 Approved: {result.get('ok', False)}")
        except Exception as e:
            print(f"❌ Error: {e}")
        print("-" * 50)


def main():
    """Main test function"""
    print("🧪 Testing RAG Integration")
    print("=" * 50)
    
    # Setup logging
    setup_logging(settings.log_level)
    
    try:
        # Test basic retrieval
        test_retrieval()
        
        # Test full agent workflow
        test_agent_with_rag()
        
        print("\n✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\n💡 Make sure you have:")
        print("   - Run scripts/init_rag.py first")
        print("   - OPENAI_API_KEY set in your .env file")
        print("   - Required dependencies installed")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
