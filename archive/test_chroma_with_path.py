import sys

# 手动添加用户站点目录到sys.path
user_site = r"C:\Users\Administrator\AppData\Roaming\Python\Python314\site-packages"
if user_site not in sys.path:
    print(f"Adding user site directory to sys.path: {user_site}")
    sys.path.append(user_site)
else:
    print(f"User site directory already in sys.path: {user_site}")

# 尝试导入chromadb
try:
    import chromadb
    print("ChromaDB installed successfully!")
    print(f"ChromaDB version: {chromadb.__version__}")
    
    # 验证基本功能
    print("\nTesting basic ChromaDB functionality...")
    # 创建客户端
    client = chromadb.Client()
    print("✓ Client created successfully")
    
    # 创建集合
    collection = client.create_collection(name="test_collection")
    print("✓ Collection created successfully")
    
    # 添加文档
    collection.add(
        documents=["This is a test document"],
        metadatas=[{"source": "test"}],
        ids=["1"]
    )
    print("✓ Document added successfully")
    
    # 执行查询
    results = collection.query(
        query_texts=["test"],
        n_results=1
    )
    print("✓ Query executed successfully")
    print(f"Query results: {results}")
    
    print("\nAll tests passed! ChromaDB is working correctly.")
    
except ImportError as e:
    print(f"ChromaDB is not installed: {e}")
    # 检查用户站点目录是否存在chromadb
    import os
    if os.path.exists(user_site):
        print(f"\nChecking user site directory: {user_site}")
        files = os.listdir(user_site)
        print(f"Files in user site directory: {files}")
        if any("chroma" in f.lower() for f in files):
            print("ChromaDB files found, but cannot be imported.")
        else:
            print("No ChromaDB files found in user site directory.")
    else:
        print(f"User site directory does not exist: {user_site}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()