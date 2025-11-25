"""
Documentation Loading Agent - Universal Memory Bridge
Loads framework documentation into ChromaDB using Context7 and Docling
Makes knowledge available to Claude, Gemini, OpenAI, and all AI platforms
"""

import os
import requests
from typing import List, Dict, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DocumentationLoadingAgent:
    """
    Intelligent agent for loading framework documentation into ChromaDB
    Uses Context7 for documentation access and Docling for processing
    """
    
    def __init__(
        self,
        chroma_host: str = "localhost",
        chroma_port: int = 8000,
        context7_api_key: Optional[str] = None,
        docling_enabled: bool = True
    ):
        """Initialize the Documentation Loading Agent"""
        
        # ChromaDB client
        self.chroma_client = chromadb.HttpClient(
            host=chroma_host,
            port=chroma_port,
            settings=Settings(anonymized_telemetry=False)
        )
        
        self.context7_api_key = context7_api_key or os.getenv("CONTEXT7_API_KEY")
        self.docling_enabled = docling_enabled
        
        logger.info(f"🚀 Documentation Loading Agent initialized")
        logger.info(f"📊 ChromaDB: {chroma_host}:{chroma_port}")
        logger.info(f"🔑 Context7: {'Enabled' if self.context7_api_key else 'Disabled'}")
        logger.info(f"📄 Docling: {'Enabled' if docling_enabled else 'Disabled'}")
    
    def get_or_create_collection(self, collection_name: str) -> chromadb.Collection:
        """Get or create a ChromaDB collection"""
        try:
            collection = self.chroma_client.get_collection(name=collection_name)
            logger.info(f"✅ Found existing collection: {collection_name}")
        except:
            collection = self.chroma_client.create_collection(
                name=collection_name,
                metadata={
                    "created_at": datetime.now().isoformat(),
                    "agent": "DocumentationLoadingAgent",
                    "purpose": "framework_documentation"
                }
            )
            logger.info(f"✨ Created new collection: {collection_name}")
        
        return collection
    
    def load_framework_from_context7(
        self,
        framework_name: str,
        documentation_url: str,
        collection_name: str = "documentation_library"
    ) -> Dict:
        """
        Load framework documentation from Context7
        
        Args:
            framework_name: Name of the framework (e.g., "FastAPI", "React")
            documentation_url: Official documentation URL
            collection_name: ChromaDB collection to store in
        
        Returns:
            Dict with loading statistics
        """
        logger.info(f"📚 Loading {framework_name} documentation from Context7...")
        
        if not self.context7_api_key:
            logger.error("❌ Context7 API key not configured")
            return {"error": "Context7 API key required"}
        
        collection = self.get_or_create_collection(collection_name)
        
        # Context7 API request
        headers = {
            "Authorization": f"Bearer {self.context7_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "url": documentation_url,
            "framework": framework_name,
            "extract_code": True,
            "extract_examples": True,
            "chunk_size": 1000,
            "overlap": 200
        }
        
        try:
            response = requests.post(
                "https://api.context7.ai/v1/extract",
                headers=headers,
                json=payload,
                timeout=300
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract documents from Context7 response
            documents = data.get("documents", [])
            
            if not documents:
                logger.warning(f"⚠️ No documents extracted from {documentation_url}")
                return {"framework": framework_name, "documents_loaded": 0}
            
            # Prepare for ChromaDB
            ids = []
            texts = []
            metadatas = []
            
            for idx, doc in enumerate(documents):
                doc_id = f"{framework_name.lower()}_{idx}_{datetime.now().timestamp()}"
                ids.append(doc_id)
                texts.append(doc.get("content", ""))
                metadatas.append({
                    "framework": framework_name,
                    "source": documentation_url,
                    "type": doc.get("type", "documentation"),
                    "section": doc.get("section", "unknown"),
                    "has_code": doc.get("has_code", False),
                    "trust_score": doc.get("trust_score", 8),
                    "loaded_at": datetime.now().isoformat()
                })
            
            # Add to ChromaDB
            collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas
            )
            
            logger.info(f"✅ Loaded {len(documents)} documents for {framework_name}")
            
            return {
                "framework": framework_name,
                "documents_loaded": len(documents),
                "collection": collection_name,
                "source": documentation_url,
                "timestamp": datetime.now().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Context7 API error: {e}")
            return {"error": str(e), "framework": framework_name}
        except Exception as e:
            logger.error(f"❌ Error loading {framework_name}: {e}")
            return {"error": str(e), "framework": framework_name}
    
    def load_local_documentation(
        self,
        framework_name: str,
        file_path: str,
        collection_name: str = "documentation_library",
        use_docling: bool = True
    ) -> Dict:
        """
        Load documentation from local files using Docling
        
        Args:
            framework_name: Name of the framework
            file_path: Path to documentation file (PDF, MD, HTML, etc.)
            collection_name: ChromaDB collection to store in
            use_docling: Whether to use Docling for processing
        
        Returns:
            Dict with loading statistics
        """
        logger.info(f"📄 Loading {framework_name} from local file: {file_path}")
        
        if not Path(file_path).exists():
            logger.error(f"❌ File not found: {file_path}")
            return {"error": "File not found", "framework": framework_name}
        
        collection = self.get_or_create_collection(collection_name)
        
        try:
            if use_docling and self.docling_enabled:
                # Use Docling for intelligent document processing
                from docling.document_converter import DocumentConverter
                
                converter = DocumentConverter()
                result = converter.convert(file_path)
                
                # Extract structured content
                documents = []
                for element in result.document.iterate_items():
                    if hasattr(element, 'text') and element.text:
                        documents.append({
                            "content": element.text,
                            "type": element.label if hasattr(element, 'label') else "text",
                            "section": getattr(element, 'section', 'unknown')
                        })
            else:
                # Simple file reading fallback
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple chunking
                chunk_size = 1000
                chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
                documents = [{"content": chunk, "type": "text", "section": "unknown"} for chunk in chunks]
            
            # Prepare for ChromaDB
            ids = []
            texts = []
            metadatas = []
            
            for idx, doc in enumerate(documents):
                doc_id = f"{framework_name.lower()}_local_{idx}_{datetime.now().timestamp()}"
                ids.append(doc_id)
                texts.append(doc.get("content", ""))
                metadatas.append({
                    "framework": framework_name,
                    "source": file_path,
                    "type": doc.get("type", "documentation"),
                    "section": doc.get("section", "unknown"),
                    "trust_score": 7,
                    "loaded_at": datetime.now().isoformat()
                })
            
            # Add to ChromaDB
            collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas
            )
            
            logger.info(f"✅ Loaded {len(documents)} chunks for {framework_name}")
            
            return {
                "framework": framework_name,
                "documents_loaded": len(documents),
                "collection": collection_name,
                "source": file_path,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error loading {framework_name}: {e}")
            return {"error": str(e), "framework": framework_name}
    
    def bulk_load_frameworks(
        self,
        frameworks: List[Dict[str, str]],
        collection_name: str = "documentation_library"
    ) -> List[Dict]:
        """
        Load multiple frameworks in batch
        
        Args:
            frameworks: List of dicts with 'name' and 'url' keys
            collection_name: ChromaDB collection to store in
        
        Returns:
            List of loading results
        """
        logger.info(f"🔄 Bulk loading {len(frameworks)} frameworks...")
        
        results = []
        for framework in frameworks:
            name = framework.get("name")
            url = framework.get("url")
            
            if not name or not url:
                logger.warning(f"⚠️ Skipping invalid framework entry: {framework}")
                continue
            
            result = self.load_framework_from_context7(
                framework_name=name,
                documentation_url=url,
                collection_name=collection_name
            )
            results.append(result)
        
        # Summary
        successful = sum(1 for r in results if "error" not in r)
        total_docs = sum(r.get("documents_loaded", 0) for r in results)
        
        logger.info(f"🎉 Bulk load complete: {successful}/{len(frameworks)} frameworks, {total_docs} total documents")
        
        return results
    
    def verify_documentation(
        self,
        framework_name: str,
        collection_name: str = "documentation_library"
    ) -> Dict:
        """
        Verify that framework documentation is accessible
        
        Args:
            framework_name: Name of the framework to verify
            collection_name: ChromaDB collection to check
        
        Returns:
            Dict with verification results
        """
        logger.info(f"🔍 Verifying {framework_name} documentation...")
        
        try:
            collection = self.chroma_client.get_collection(name=collection_name)
            
            # Query for this framework
            results = collection.query(
                query_texts=[f"{framework_name} documentation"],
                n_results=5,
                where={"framework": framework_name}
            )
            
            doc_count = len(results['ids'][0]) if results['ids'] else 0
            
            logger.info(f"✅ Found {doc_count} documents for {framework_name}")
            
            return {
                "framework": framework_name,
                "available": doc_count > 0,
                "document_count": doc_count,
                "collection": collection_name
            }
            
        except Exception as e:
            logger.error(f"❌ Verification error: {e}")
            return {
                "framework": framework_name,
                "available": False,
                "error": str(e)
            }
    
    def create_documentation_index(
        self,
        collection_name: str = "documentation_library",
        output_file: Optional[str] = None
    ) -> Dict:
        """
        Create an index of all available framework documentation
        
        Args:
            collection_name: ChromaDB collection to index
            output_file: Optional file path to save index
        
        Returns:
            Dict with complete documentation index
        """
        logger.info(f"📋 Creating documentation index for {collection_name}...")
        
        try:
            collection = self.chroma_client.get_collection(name=collection_name)
            
            # Get all documents
            all_docs = collection.get()
            
            # Group by framework
            frameworks = {}
            for metadata in all_docs['metadatas']:
                fw = metadata.get('framework', 'unknown')
                if fw not in frameworks:
                    frameworks[fw] = {
                        "name": fw,
                        "document_count": 0,
                        "sources": set(),
                        "types": set()
                    }
                
                frameworks[fw]["document_count"] += 1
                frameworks[fw]["sources"].add(metadata.get('source', 'unknown'))
                frameworks[fw]["types"].add(metadata.get('type', 'unknown'))
            
            # Convert sets to lists for JSON serialization
            for fw in frameworks.values():
                fw["sources"] = list(fw["sources"])
                fw["types"] = list(fw["types"])
            
            index = {
                "collection": collection_name,
                "total_frameworks": len(frameworks),
                "total_documents": len(all_docs['ids']),
                "frameworks": frameworks,
                "created_at": datetime.now().isoformat()
            }
            
            # Save to file if requested
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(index, f, indent=2)
                logger.info(f"💾 Index saved to {output_file}")
            
            logger.info(f"✅ Index created: {len(frameworks)} frameworks, {len(all_docs['ids'])} documents")
            
            return index
            
        except Exception as e:
            logger.error(f"❌ Index creation error: {e}")
            return {"error": str(e)}


def main():
    """Main entry point for the Documentation Loading Agent"""
    
    # Initialize agent
    agent = DocumentationLoadingAgent(
        chroma_host=os.getenv("CHROMA_HOST", "localhost"),
        chroma_port=int(os.getenv("CHROMA_PORT", "8000")),
        context7_api_key=os.getenv("CONTEXT7_API_KEY"),
        docling_enabled=True
    )
    
    # Example: Load a single framework
    # result = agent.load_framework_from_context7(
    #     framework_name="FastAPI",
    #     documentation_url="https://fastapi.tiangolo.com"
    # )
    # print(f"Loaded: {result}")
    
    # Example: Create documentation index
    index = agent.create_documentation_index(
        output_file="/data/documentation_index.json"
    )
    print(json.dumps(index, indent=2))


if __name__ == "__main__":
    main()
