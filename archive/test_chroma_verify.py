import chromadb
from chromadb.config import Settings

print("Testing ChromaDB installation...")
print(f"ChromaDB version: {chromadb.__version__}")

# Test creating a client
try:
    client = chromadb.Client(Settings(
        persist_directory="./chromadb_data",
        anonymized_telemetry=False
    ))
    print("✓ Client created successfully")
    
    # Test creating a collection
    collection = client.create_collection(name="test_collection")
    print("✓ Collection created successfully")
    
    # Test adding documents
    collection.add(
        documents=["This is a test document"],
        metadatas=[{"source": "test"}],
        ids=["1"]
    )
    print("✓ Documents added successfully")
    
    # Test querying
    results = collection.query(
        query_texts=["test"],
        n_results=1
    )
    print("✓ Query executed successfully")
    print(f"  Query results: {results}")
    
    print("\n🎉 All tests passed! ChromaDB is working correctly.")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
