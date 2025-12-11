import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.chains.retrieval_chain import create_rag_chain

def main():
    """Test retrieval system"""
    print("Testing retrieval system...\n")
    
    qa_chain = create_rag_chain()
    
    test_questions = [
        "Apa saja menu kopi yang tersedia?",
        "Bagaimana cara menjadi member Starbucks?",
        "Apakah ada promo hari ini?"
    ]
    
    for question in test_questions:
        print(f"Q: {question}")
        response = qa_chain.invoke({"input": question})
        print(f"A: {response.get('answer', 'No answer')}\n")
        print("-" * 80 + "\n")

if __name__ == "__main__":
    main()