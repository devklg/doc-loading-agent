"""
Load All Framework Documentation - Universal Memory Bridge
Loads comprehensive framework documentation into ChromaDB
Available to Claude, Gemini, OpenAI, and all AI platforms
"""

import os
import sys
import json
from agent import DocumentationLoadingAgent
from datetime import datetime

# Framework documentation URLs
FRAMEWORKS = {
    "python": {
        "name": "Python 3.12",
        "url": "https://docs.python.org/3.12/",
        "priority": 1,
        "description": "Core Python 3.12 documentation"
    },
    "pydantic": {
        "name": "Pydantic v2",
        "url": "https://docs.pydantic.dev/latest/",
        "priority": 1,
        "description": "Pydantic v2 data validation"
    },
    "fastapi": {
        "name": "FastAPI",
        "url": "https://fastapi.tiangolo.com/",
        "priority": 1,
        "description": "FastAPI web framework"
    },
    "django": {
        "name": "Django",
        "url": "https://docs.djangoproject.com/en/stable/",
        "priority": 2,
        "description": "Django web framework"
    },
    "react": {
        "name": "React 19",
        "url": "https://react.dev/",
        "priority": 1,
        "description": "React 19 documentation"
    },
    "vite": {
        "name": "Vite",
        "url": "https://vitejs.dev/",
        "priority": 2,
        "description": "Vite build tool"
    },
    "tailwind": {
        "name": "Tailwind CSS v4",
        "url": "https://tailwindcss.com/docs",
        "priority": 2,
        "description": "Tailwind CSS v4 utility framework"
    },
    "mongodb": {
        "name": "MongoDB",
        "url": "https://www.mongodb.com/docs/",
        "priority": 1,
        "description": "MongoDB database documentation"
    },
    "express": {
        "name": "Express.js",
        "url": "https://expressjs.com/",
        "priority": 2,
        "description": "Express.js Node framework"
    },
    "langchain": {
        "name": "LangChain",
        "url": "https://python.langchain.com/docs/",
        "priority": 1,
        "description": "LangChain LLM framework"
    },
    "crewai": {
        "name": "CrewAI",
        "url": "https://docs.crewai.com/",
        "priority": 1,
        "description": "CrewAI multi-agent framework"
    },
    "docker": {
        "name": "Docker",
        "url": "https://docs.docker.com/",
        "priority": 1,
        "description": "Docker containerization"
    },
    "chroma": {
        "name": "ChromaDB",
        "url": "https://docs.trychroma.com/",
        "priority": 1,
        "description": "ChromaDB vector database"
    },
    "neon": {
        "name": "Neon Postgres",
        "url": "https://neon.tech/docs/",
        "priority": 1,
        "description": "Neon serverless Postgres"
    },
    "redis": {
        "name": "Redis",
        "url": "https://redis.io/docs/",
        "priority": 1,
        "description": "Redis in-memory database"
    },
    "telnyx": {
        "name": "Telnyx",
        "url": "https://developers.telnyx.com/docs/",
        "priority": 2,
        "description": "Telnyx telephony API"
    },
    "grafana": {
        "name": "Grafana",
        "url": "https://grafana.com/docs/",
        "priority": 2,
        "description": "Grafana monitoring"
    }
}


def load_all_frameworks(agent: DocumentationLoadingAgent, priority_only: bool = False):
    """
    Load all framework documentation
    
    Args:
        agent: DocumentationLoadingAgent instance
        priority_only: If True, only load priority 1 frameworks
    """
    
    # Filter frameworks by priority if requested
    frameworks_to_load = FRAMEWORKS
    if priority_only:
        frameworks_to_load = {
            k: v for k, v in FRAMEWORKS.items() 
            if v.get("priority", 2) == 1
        }
    
    print(f"\n{'='*80}")
    print(f"🚀 UNIVERSAL MEMORY BRIDGE - DOCUMENTATION LOADING")
    print(f"{'='*80}")
    print(f"📚 Loading {len(frameworks_to_load)} frameworks into ChromaDB")
    print(f"🌐 Knowledge available to: Claude, Gemini, OpenAI, Local LLMs")
    print(f"{'='*80}\n")
    
    results = []
    successful = 0
    failed = 0
    total_docs = 0
    
    for idx, (key, framework) in enumerate(frameworks_to_load.items(), 1):
        print(f"\n[{idx}/{len(frameworks_to_load)}] Loading {framework['name']}...")
        print(f"  📖 {framework['description']}")
        print(f"  🔗 {framework['url']}")
        
        try:
            result = agent.load_framework_from_context7(
                framework_name=framework["name"],
                documentation_url=framework["url"],
                collection_name="documentation_library"
            )
            
            if "error" in result:
                print(f"  ❌ Failed: {result['error']}")
                failed += 1
            else:
                docs_loaded = result.get("documents_loaded", 0)
                print(f"  ✅ Success: {docs_loaded} documents loaded")
                successful += 1
                total_docs += docs_loaded
            
            results.append(result)
            
        except Exception as e:
            print(f"  ❌ Exception: {e}")
            failed += 1
            results.append({"framework": framework["name"], "error": str(e)})
    
    # Summary
    print(f"\n{'='*80}")
    print(f"📊 LOADING SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Successful: {successful}/{len(frameworks_to_load)}")
    print(f"❌ Failed: {failed}/{len(frameworks_to_load)}")
    print(f"📄 Total documents: {total_docs:,}")
    print(f"⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")
    
    # Save results
    results_file = f"/data/loading_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "frameworks_attempted": len(frameworks_to_load),
            "successful": successful,
            "failed": failed,
            "total_documents": total_docs,
            "results": results
        }, f, indent=2)
    
    print(f"💾 Results saved to: {results_file}\n")
    
    return results


def verify_all_frameworks(agent: DocumentationLoadingAgent):
    """Verify that all frameworks are accessible"""
    
    print(f"\n{'='*80}")
    print(f"🔍 VERIFYING FRAMEWORK DOCUMENTATION")
    print(f"{'='*80}\n")
    
    for key, framework in FRAMEWORKS.items():
        result = agent.verify_documentation(
            framework_name=framework["name"],
            collection_name="documentation_library"
        )
        
        status = "✅" if result.get("available") else "❌"
        doc_count = result.get("document_count", 0)
        print(f"{status} {framework['name']}: {doc_count} documents")
    
    print(f"\n{'='*80}\n")


def create_index(agent: DocumentationLoadingAgent):
    """Create comprehensive documentation index"""
    
    print(f"\n{'='*80}")
    print(f"📋 CREATING DOCUMENTATION INDEX")
    print(f"{'='*80}\n")
    
    index = agent.create_documentation_index(
        collection_name="documentation_library",
        output_file="/data/documentation_index.json"
    )
    
    print(f"📊 Total Frameworks: {index.get('total_frameworks', 0)}")
    print(f"📄 Total Documents: {index.get('total_documents', 0):,}")
    print(f"💾 Index saved to: /data/documentation_index.json")
    print(f"\n{'='*80}\n")
    
    return index


def main():
    """Main entry point"""
    
    # Check for Context7 API key
    if not os.getenv("CONTEXT7_API_KEY"):
        print("⚠️  WARNING: CONTEXT7_API_KEY not set")
        print("   Set environment variable: export CONTEXT7_API_KEY='your-key'")
        print("   Or add to .env file\n")
    
    # Initialize agent
    print("🤖 Initializing Documentation Loading Agent...\n")
    agent = DocumentationLoadingAgent(
        chroma_host=os.getenv("CHROMA_HOST", "localhost"),
        chroma_port=int(os.getenv("CHROMA_PORT", "8000")),
        context7_api_key=os.getenv("CONTEXT7_API_KEY"),
        docling_enabled=True
    )
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "load":
            # Load all frameworks
            priority_only = "--priority" in sys.argv
            load_all_frameworks(agent, priority_only=priority_only)
            
        elif command == "verify":
            # Verify all frameworks
            verify_all_frameworks(agent)
            
        elif command == "index":
            # Create index
            create_index(agent)
            
        elif command == "all":
            # Do everything
            load_all_frameworks(agent)
            verify_all_frameworks(agent)
            create_index(agent)
            
        else:
            print(f"Unknown command: {command}")
            print_usage()
    else:
        print_usage()


def print_usage():
    """Print usage information"""
    print("""
Usage: python load_frameworks.py <command> [options]

Commands:
  load          Load all framework documentation
  load --priority   Load only priority 1 frameworks
  verify        Verify all frameworks are accessible
  index         Create documentation index
  all           Load, verify, and index

Examples:
  python load_frameworks.py load
  python load_frameworks.py load --priority
  python load_frameworks.py verify
  python load_frameworks.py index
  python load_frameworks.py all
    """)


if __name__ == "__main__":
    main()
