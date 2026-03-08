
from chroma_utils import KnowledgeBase, SimpleEmbeddingGenerator, batch_add_documents

print("=" * 60)
print("ChromaDB Enhanced Demo")
print("=" * 60)

print("\n1. Testing Simple Embedding Generator")
print("=" * 60)

embedding_gen = SimpleEmbeddingGenerator(dimension=128)

text1 = "Python is a high-level programming language"
text2 = "JavaScript is also a popular programming language"
text3 = "ChromaDB is a vector database"

emb1 = embedding_gen.generate_embedding(text1)
emb2 = embedding_gen.generate_embedding(text2)
emb3 = embedding_gen.generate_embedding(text3)

print(f"Text 1: {text1}")
print(f"Embedding dimension: {len(emb1)}")
print(f"First 5 values: {emb1[:5]}")

import numpy as np
similarity1_2 = np.dot(emb1, emb2)
similarity1_3 = np.dot(emb1, emb3)

print(f"\nSimilarity between text1 and text2: {similarity1_2:.4f}")
print(f"Similarity between text1 and text3: {similarity1_3:.4f}")

print("\n2. Testing Knowledge Base (In-Memory)")
print("=" * 60)

kb = KnowledgeBase(name="demo_kb_memory", embedding_dim=128)

print("\nAdding documents to knowledge base...")
doc_id1 = kb.add_document(
    "Python is a high-level programming language known for its simple syntax, widely used in data analysis, web development, and AI",
    metadata={"category": "programming", "language": "Python"}
)

doc_id2 = kb.add_document(
    "ChromaDB is an open-source vector database designed for AI applications, supporting similarity search and persistent storage",
    metadata={"category": "database", "type": "vector"}
)

doc_id3 = kb.add_document(
    "Machine learning is a branch of AI that learns patterns from data through algorithms to make predictions",
    metadata={"category": "ai", "field": "machine_learning"}
)

doc_id4 = kb.add_document(
    "JavaScript is a frontend programming language mainly used for web interaction and development",
    metadata={"category": "programming", "language": "JavaScript"}
)

print(f"Added {kb.count()} documents")

print("\nQuerying knowledge base: 'vector database'")
results = kb.query("vector database", n_results=3)

for i, doc in enumerate(results['documents'][0]):
    distance = results['distances'][0][i]
    similarity = 1 - distance
    metadata = results['metadatas'][0][i] if results['metadatas'] else None
    print(f"\nResult {i+1}:")
    print(f"  Content: {doc}")
    print(f"  Similarity: {similarity:.4f}")
    if metadata:
        print(f"  Metadata: {metadata}")

print("\n" + "-" * 60)
print("Filtered query: 'programming language' (category='programming')")
results_filtered = kb.query("programming language", n_results=5, where={"category": "programming"})

print(f"Found {len(results_filtered['documents'][0])} matching results:")
for i, doc in enumerate(results_filtered['documents'][0]):
    distance = results_filtered['distances'][0][i]
    print(f"  {i+1}. {doc[:50]}... (similarity: {1-distance:.4f})")

print("\n" + "-" * 60)
print("Updating a document...")
kb.update_document(
    doc_id1,
    document="Python is a high-level programming language known for its simple syntax, widely used in data analysis, web development, AI, and scientific computing",
    metadata={"category": "programming", "language": "Python", "updated": True}
)
print("Document updated successfully")

print("\n" + "-" * 60)
print("Getting all documents:")
all_docs = kb.get_all_documents()
for i, doc_id in enumerate(all_docs['ids']):
    print(f"  {doc_id}: {all_docs['documents'][i][:60]}...")

print("\n" + "-" * 60)
print("Deleting a document...")
kb.delete_document(doc_id4)
print(f"Document deleted, current count: {kb.count()}")

kb.delete()
print("\nIn-memory knowledge base cleaned up")

print("\n3. Testing Persistent Storage")
print("=" * 60)

kb_persist = KnowledgeBase(
    name="demo_kb_persist",
    persist_directory="./chroma_db",
    embedding_dim=128
)

print("\nAdding documents to persistent knowledge base...")
kb_persist.add_document("Persistent storage saves data to disk", metadata={"type": "persistence"})
kb_persist.add_document("Data remains after restarting the program", metadata={"type": "persistence"})
kb_persist.add_document("This is a very useful feature", metadata={"type": "feature"})

print(f"Added {kb_persist.count()} documents to persistent storage")

print("\nQuerying persistent knowledge base: 'data saving'")
results_persist = kb_persist.query("data saving", n_results=2)
for i, doc in enumerate(results_persist['documents'][0]):
    print(f"  {i+1}. {doc} (similarity: {1-results_persist['distances'][0][i]:.4f})")

print("\nPersistent knowledge base saved to ./chroma_db directory")

print("\n4. Testing Batch Add")
print("=" * 60)

kb_batch = KnowledgeBase(name="demo_kb_batch", embedding_dim=128)

batch_docs = []
for i in range(1, 11):
    batch_docs.append({
        'content': f"This is batch document {i}, about data science and machine learning",
        'metadata': {"batch": True, "index": i},
        'id': f"batch_doc_{i}"
    })

print(f"\nBatch adding {len(batch_docs)} documents...")
batch_add_documents(kb_batch, batch_docs, batch_size=3)

print(f"Batch add complete, current count: {kb_batch.count()}")

print("\nQuerying batch documents: 'data science'")
results_batch = kb_batch.query("data science", n_results=5)
for i, doc in enumerate(results_batch['documents'][0]):
    metadata = results_batch['metadatas'][0][i]
    print(f"  {i+1}. {doc} (index: {metadata['index']}, similarity: {1-results_batch['distances'][0][i]:.4f})")

kb_batch.delete()
print("\nBatch test knowledge base cleaned up")

print("\n" + "=" * 60)
print("All features demonstrated!")
print("=" * 60)
print("\nTips:")
print("- Persistent data is saved in ./chroma_db directory")
print("- You can load the persistent knowledge base next time")
print("- Check chroma_utils.py for more available functions")

