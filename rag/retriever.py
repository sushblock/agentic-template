import os
from typing import List
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from ops.config.settings import settings


class ChromaRetriever:
    def __init__(self):
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.openai_api_key,
            model="text-embedding-3-small"
        )
        
        # Initialize ChromaDB
        self.vectorstore = Chroma(
            persist_directory=settings.chroma_persist_directory,
            collection_name=settings.chroma_collection_name,
            embedding_function=self.embeddings
        )
        
        # Text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def add_documents(self, documents: List[str], metadatas: List[dict] = None):
        """Add documents to the vector store"""
        if metadatas is None:
            metadatas = [{}] * len(documents)
        
        # Create Document objects
        docs = [Document(page_content=doc, metadata=meta) for doc, meta in zip(documents, metadatas)]
        
        # Split documents into chunks
        split_docs = self.text_splitter.split_documents(docs)
        
        # Add to vector store
        self.vectorstore.add_documents(split_docs)
        self.vectorstore.persist()

    def retrieve(self, query: str, k: int = 3) -> str:
        """Retrieve relevant documents for a query"""
        try:
            # Perform similarity search
            docs = self.vectorstore.similarity_search(query, k=k)
            
            if not docs:
                return f"[RAG CONTEXT] No relevant documents found for: {query}"
            
            # Combine retrieved documents
            context_parts = []
            for i, doc in enumerate(docs, 1):
                context_parts.append(f"Document {i}:\n{doc.page_content}")
                if doc.metadata:
                    context_parts.append(f"Metadata: {doc.metadata}")
            
            return "\n\n".join(context_parts)
            
        except Exception as e:
            return f"[RAG CONTEXT] Error retrieving documents: {str(e)}"


# Global retriever instance
_retriever = None

def get_retriever() -> ChromaRetriever:
    """Get or create the global retriever instance"""
    global _retriever
    if _retriever is None:
        _retriever = ChromaRetriever()
    return _retriever

def retrieve(query: str) -> str:
    """Main retrieve function - interface for the agent"""
    retriever = get_retriever()
    return retriever.retrieve(query)