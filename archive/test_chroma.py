try:
    import chromadb
    print("ChromaDB installed successfully!")
    print(f"ChromaDB version: {chromadb.__version__}")
except ImportError:
    print("ChromaDB is not installed.")
except Exception as e:
    print(f"Error: {e}")
