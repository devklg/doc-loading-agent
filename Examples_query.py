"""
Example: Query Documentation from Different AI Platforms
Demonstrates how Claude, OpenAI, Gemini, and others can access the same knowledge base
"""

import os
import chromadb
from typing import List, Dict

# Initialize ChromaDB client
client = chromadb.HttpClient(
    host=os.getenv("CHROMA_HOST", "localhost"),
    port=int(os.getenv("CHROMA_PORT", "8000"))
)

collection = client.get_collection("documentation_library")


def query_documentation(query: str, framework: str = None, n_results: int = 3) -> Dict:
    """
    Query the documentation collection
    
    Args:
        query: Natural language query
        framework: Optional framework filter
        n_results: Number of results to return
    
    Returns:
        Dict with query results
    """
    
    # Build query parameters
    kwargs = {
        "query_texts": [query],
        "n_results": n_results
    }
    
    # Add framework filter if specified
    if framework:
        kwargs["where"] = {"framework": framework}
    
    # Query ChromaDB
    results = collection.query(**kwargs)
    
    return {
        "query": query,
        "framework": framework,
        "results": results
    }


# ============================================================================
# EXAMPLE 1: Claude via MCP
# ============================================================================
def example_claude_mcp():
    """
    Claude automatically has access via MCP tools
    No special setup needed - Claude can query directly through MCP
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Claude via MCP")
    print("="*80)
    print("""
Claude has built-in access through MCP tools:
- Just ask Claude questions about any loaded framework
- Claude queries ChromaDB automatically
- No additional code needed

Example conversation:
User: "Show me how to create a FastAPI route with Pydantic validation"
Claude: [Uses MCP tools to query ChromaDB, gets relevant docs, responds]
    """)


# ============================================================================
# EXAMPLE 2: OpenAI with Retrieved Context
# ============================================================================
def example_openai():
    """
    Query documentation and use with OpenAI
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: OpenAI with ChromaDB Context")
    print("="*80)
    
    # Query documentation
    results = query_documentation(
        query="How do I create a route in FastAPI with request validation?",
        framework="FastAPI",
        n_results=3
    )
    
    # Format context for OpenAI
    context = "\n\n".join(results['results']['documents'][0])
    
    print("\nRetrieved Context:")
    print("-" * 80)
    print(context[:500] + "..." if len(context) > 500 else context)
    print("-" * 80)
    
    # Example OpenAI API call (commented to avoid actual API call)
    print("\nOpenAI API Call Example:")
    print("""
import openai

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "You are a FastAPI expert. Use the provided documentation context to answer questions."
        },
        {
            "role": "user",
            "content": f'''
Context from FastAPI documentation:
{context}

Question: How do I create a route with request validation?
'''
        }
    ]
)

print(response.choices[0].message.content)
    """)


# ============================================================================
# EXAMPLE 3: Google Gemini with Retrieved Context
# ============================================================================
def example_gemini():
    """
    Query documentation and use with Google Gemini
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Google Gemini with ChromaDB Context")
    print("="*80)
    
    # Query documentation
    results = query_documentation(
        query="React hooks useState and useEffect examples",
        framework="React 19",
        n_results=3
    )
    
    # Format context for Gemini
    context = "\n\n".join(results['results']['documents'][0])
    
    print("\nRetrieved Context:")
    print("-" * 80)
    print(context[:500] + "..." if len(context) > 500 else context)
    print("-" * 80)
    
    # Example Gemini API call (commented to avoid actual API call)
    print("\nGemini API Call Example:")
    print("""
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

prompt = f'''
You are a React expert. Use the following documentation context:

{context}

Question: Explain how to use useState and useEffect hooks with examples.
'''

response = model.generate_content(prompt)
print(response.text)
    """)


# ============================================================================
# EXAMPLE 4: Local LLM (Ollama) with Retrieved Context
# ============================================================================
def example_local_llm():
    """
    Query documentation and use with local LLM
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Local LLM (Ollama) with ChromaDB Context")
    print("="*80)
    
    # Query documentation
    results = query_documentation(
        query="Docker compose configuration for Python applications",
        framework="Docker",
        n_results=3
    )
    
    # Format context for local LLM
    context = "\n\n".join(results['results']['documents'][0])
    
    print("\nRetrieved Context:")
    print("-" * 80)
    print(context[:500] + "..." if len(context) > 500 else context)
    print("-" * 80)
    
    # Example Ollama API call (commented to avoid actual API call)
    print("\nOllama API Call Example:")
    print("""
import ollama

response = ollama.chat(
    model='llama3',
    messages=[
        {
            'role': 'system',
            'content': 'You are a Docker expert. Use the provided documentation to answer questions.'
        },
        {
            'role': 'user',
            'content': f'''
Documentation context:
{context}

Question: How do I create a docker-compose.yml for a Python application?
'''
        }
    ]
)

print(response['message']['content'])
    """)


# ============================================================================
# EXAMPLE 5: LangChain with ChromaDB Retriever
# ============================================================================
def example_langchain():
    """
    LangChain has native ChromaDB integration
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: LangChain with ChromaDB Retriever")
    print("="*80)
    
    print("""
LangChain has native ChromaDB support:

from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Connect to existing ChromaDB
vectorstore = Chroma(
    collection_name="documentation_library",
    persist_directory="/path/to/chromadb",
    embedding_function=embedding_function
)

# Create retrieval chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )
)

# Query with automatic retrieval
response = qa_chain.run("How do I use Pydantic models in FastAPI?")
print(response)
    """)


# ============================================================================
# EXAMPLE 6: CrewAI Agent with Documentation Access
# ============================================================================
def example_crewai():
    """
    CrewAI agents can use ChromaDB for knowledge
    """
    print("\n" + "="*80)
    print("EXAMPLE 6: CrewAI Agent with Documentation Access")
    print("="*80)
    
    print("""
CrewAI agents can query the documentation:

from crewai import Agent, Task, Crew
from langchain.vectorstores import Chroma

# Setup ChromaDB retriever
vectorstore = Chroma(
    collection_name="documentation_library",
    persist_directory="/path/to/chromadb"
)

# Create agent with documentation access
developer = Agent(
    role='Senior Developer',
    goal='Help users with framework questions',
    backstory='Expert in multiple frameworks with access to comprehensive documentation',
    tools=[vectorstore.as_retriever()]
)

# Create task
task = Task(
    description='Explain how to create a MongoDB connection in Python',
    agent=developer
)

# Run crew
crew = Crew(agents=[developer], tasks=[task])
result = crew.kickoff()
print(result)
    """)


# ============================================================================
# EXAMPLE 7: Direct Python Query (Any Custom Agent)
# ============================================================================
def example_custom_agent():
    """
    Any custom Python agent can query directly
    """
    print("\n" + "="*80)
    print("EXAMPLE 7: Custom Python Agent with Direct ChromaDB Access")
    print("="*80)
    
    # Query documentation
    results = query_documentation(
        query="How to connect to MongoDB with async support?",
        framework="MongoDB",
        n_results=3
    )
    
    print("\nDirect ChromaDB Query:")
    print("-" * 80)
    
    for idx, (doc, metadata) in enumerate(zip(
        results['results']['documents'][0],
        results['results']['metadatas'][0]
    ), 1):
        print(f"\nResult {idx}:")
        print(f"Framework: {metadata.get('framework')}")
        print(f"Source: {metadata.get('source')}")
        print(f"Content: {doc[:200]}...")
    
    print("\n" + "-" * 80)
    print("\nAny custom agent can:")
    print("1. Connect to ChromaDB")
    print("2. Query the documentation_library collection")
    print("3. Use results with any LLM or processing logic")
    print("4. Build custom RAG pipelines")


# ============================================================================
# Run All Examples
# ============================================================================
def main():
    print("\n" + "="*80)
    print("UNIVERSAL MEMORY BRIDGE - MULTI-PLATFORM ACCESS EXAMPLES")
    print("="*80)
    print("\nDemonstrating how different AI platforms access the same knowledge base")
    print("All examples use the SAME ChromaDB documentation_library collection")
    
    example_claude_mcp()
    example_openai()
    example_gemini()
    example_local_llm()
    example_langchain()
    example_crewai()
    example_custom_agent()
    
    print("\n" + "="*80)
    print("🎉 UNIVERSAL ACCESS CONFIRMED!")
    print("="*80)
    print("\nKey Benefits:")
    print("✅ Load documentation ONCE")
    print("✅ Access from ANY AI platform")
    print("✅ No vendor lock-in")
    print("✅ Consistent knowledge across all agents")
    print("✅ Update once, everyone benefits")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
