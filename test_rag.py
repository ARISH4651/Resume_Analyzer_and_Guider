"""
Test script to debug RAG functionality
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag_utility import answer_question

print("="*50)
print("Testing RAG with question: 'What is ATS?'")
print("="*50)

try:
    answer = answer_question("What is ATS?")
    print("\n" + "="*50)
    print("ANSWER RECEIVED:")
    print("="*50)
    print(answer)
    print("="*50)
    print(f"\nAnswer type: {type(answer)}")
    print(f"Answer length: {len(answer) if answer else 0} characters")
except Exception as e:
    print(f"\nERROR: {str(e)}")
    import traceback
    traceback.print_exc()
