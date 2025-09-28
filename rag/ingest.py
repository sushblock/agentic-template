from typing import Iterable, List, Dict
from rag.retriever import get_retriever
import os
from pathlib import Path


def ingest_documents(documents: List[str], metadatas: List[Dict] = None):
    """Ingest documents into the vector store"""
    retriever = get_retriever()
    retriever.add_documents(documents, metadatas)
    print(f"[ingest] Added {len(documents)} documents to vector store")


def ingest_from_files(file_paths: List[str]):
    """Ingest documents from file paths"""
    documents = []
    metadatas = []
    
    for file_path in file_paths:
        try:
            path = Path(file_path)
            if not path.exists():
                print(f"[ingest] File not found: {file_path}")
                continue
                
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                documents.append(content)
                metadatas.append({
                    "source": str(path),
                    "filename": path.name,
                    "file_type": path.suffix
                })
                print(f"[ingest] Loaded {path.name} ({len(content)} chars)")
                
        except Exception as e:
            print(f"[ingest] Error loading {file_path}: {e}")
    
    if documents:
        ingest_documents(documents, metadatas)
    else:
        print("[ingest] No documents to ingest")


def ingest_sample_data():
    """Ingest sample business documents for testing"""
    sample_docs = [
        {
            "content": """
            Purchase Order Policy
            
            All purchase orders over $10,000 require manager approval. 
            Standard lead times for steel products are 3-5 business days.
            Emergency orders can be expedited for an additional 25% fee.
            
            Approved vendors:
            - SteelCorp Inc. (steel rods, beams)
            - MetalWorks Ltd. (aluminum sheets, pipes)
            - FastSupply Co. (emergency orders, same-day delivery)
            """,
            "metadata": {"type": "policy", "category": "purchasing", "version": "1.2"}
        },
        {
            "content": """
            Inventory Management Guidelines
            
            Current stock levels as of last update:
            - Steel rods (10mm): 500 units
            - Steel rods (12mm): 300 units  
            - Aluminum sheets (2mm): 150 units
            - Aluminum sheets (3mm): 200 units
            
            Reorder points:
            - Steel rods: 100 units
            - Aluminum sheets: 50 units
            
            Storage locations:
            - Warehouse A: Steel products
            - Warehouse B: Aluminum products
            """,
            "metadata": {"type": "inventory", "category": "warehouse", "last_updated": "2024-01-15"}
        },
        {
            "content": """
            Safety Protocols for Material Handling
            
            Personal Protective Equipment (PPE) required:
            - Safety glasses for all operations
            - Steel-toed boots in warehouse areas
            - Hard hats in construction zones
            - Gloves when handling sharp materials
            
            Lifting guidelines:
            - Maximum single person lift: 50 lbs
            - Use mechanical assistance for heavier items
            - Team lift required for items over 100 lbs
            
            Emergency procedures:
            - Report injuries immediately to supervisor
            - First aid station located in main office
            - Emergency contact: 911 for serious injuries
            """,
            "metadata": {"type": "safety", "category": "procedures", "effective_date": "2024-01-01"}
        },
        {
            "content": """
            Quality Control Standards
            
            Material specifications:
            - Steel rods must meet ASTM A36 standards
            - Aluminum sheets must be 6061-T6 grade minimum
            - All materials must have valid certificates of compliance
            
            Inspection procedures:
            - Visual inspection for surface defects
            - Dimensional checks using calibrated tools
            - Random sampling: 10% of each batch
            - Document all findings in QC report
            
            Rejection criteria:
            - Surface cracks or deep scratches
            - Dimensional tolerance > 0.1mm
            - Missing or invalid certificates
            """,
            "metadata": {"type": "quality", "category": "standards", "revision": "2.1"}
        }
    ]
    
    documents = [doc["content"] for doc in sample_docs]
    metadatas = [doc["metadata"] for doc in sample_docs]
    
    ingest_documents(documents, metadatas)
    print("[ingest] Sample business documents ingested successfully")


def ingest(docs: Iterable[str]):
    """Legacy function for backward compatibility"""
    documents = list(docs)
    ingest_documents(documents)  