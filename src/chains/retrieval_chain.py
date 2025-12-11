from langchain_core.output_parsers import StrOutputParser
from src.llm.gemini_llm import get_llm
from src.chains.prompts import get_prompt_template
from src.vectorstore.qdrant_manager import QdrantManager
from src.config.settings import Settings

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_chain():
    """Create RAG chain for question answering dengan dukungan chat history"""
    llm = get_llm()
    prompt = get_prompt_template()

    qdrant_manager = QdrantManager()
    vectorstore = qdrant_manager.get_vectorstore()

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": Settings.TOP_K}
    )

    # Chain sekarang mengharapkan input dict: {"input": ..., "chat_history": ...}
    rag_chain = (
        {
            "context": lambda d: format_docs(retriever.invoke(d["input"])),
            "input": lambda d: d["input"],
            "chat_history": lambda d: d.get("chat_history", ""),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    class RAGChainWrapper:
        def __init__(self, chain, retriever):
            self.chain = chain
            self.retriever = retriever

        def invoke(self, inputs):
            """Invoke chain and return result with source documents"""
            query = inputs.get("input") or inputs.get("query")
            chat_history = inputs.get("chat_history", "")

            # Ambil dokumen untuk RAG
            docs = self.retriever.invoke(query)

            # Panggil chain dengan input + history
            answer = self.chain.invoke({
                "input": query,
                "chat_history": chat_history,
            })

            return {
                "answer": answer,
                "source_documents": docs,
                "context": docs,
            }

    return RAGChainWrapper(rag_chain, retriever)
