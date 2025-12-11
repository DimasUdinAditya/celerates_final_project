from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.llm import get_llm
from src.chains.prompts import get_prompt_template
from src.vectorstore.qdrant_manager import QdrantManager
from src.config.settings import Settings

def format_docs(docs):
    """Format retrieved documents into a single string"""
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_chain():
    """Create RAG chain for question answering"""
    
    llm = get_llm()
    prompt = get_prompt_template()
    
    qdrant_manager = QdrantManager()
    vectorstore = qdrant_manager.get_vectorstore()
    
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": Settings.TOP_K}
    )
    
    # Buat chain secara manual menggunakan LCEL (LangChain Expression Language)
    rag_chain = (
        {
            "context": retriever | format_docs,
            "input": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # Wrapper untuk mengembalikan format yang konsisten
    class RAGChainWrapper:
        def __init__(self, chain, retriever):
            self.chain = chain
            self.retriever = retriever
        
        def invoke(self, inputs):
            """Invoke chain and return result with source documents"""
            query = inputs.get("input") or inputs.get("query")
            
            # Get retrieved documents - gunakan invoke() bukan get_relevant_documents()
            docs = self.retriever.invoke(query)
            
            # Get answer from chain
            answer = self.chain.invoke(query)
            
            return {
                "answer": answer,
                "source_documents": docs,
                "context": docs
            }
    
    return RAGChainWrapper(rag_chain, retriever)