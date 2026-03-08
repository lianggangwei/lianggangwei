import chromadb

print("=== 测试ChromaDB基本功能 ===")

# 1. 测试导入
print("1. 测试导入:")
print(f"ChromaDB版本: {chromadb.__version__}")

# 2. 测试创建客户端
print("\n2. 测试创建客户端:")
try:
    client = chromadb.Client()
    print("✅ 客户端创建成功")
except Exception as e:
    print(f"❌ 客户端创建失败: {e}")

# 3. 测试创建集合
print("\n3. 测试创建集合:")
try:
    collection = client.create_collection(name="test_collection")
    print("✅ 集合创建成功")
except Exception as e:
    print(f"❌ 集合创建失败: {e}")

# 4. 测试添加文档
print("\n4. 测试添加文档:")
try:
    collection.add(
        documents=["这是第一个文档", "这是第二个文档", "这是第三个文档"],
        ids=["1", "2", "3"]
    )
    print("✅ 文档添加成功")
except Exception as e:
    print(f"❌ 文档添加失败: {e}")

# 5. 测试查询
print("\n5. 测试查询:")
try:
    results = collection.query(
        query_texts=["第一个"],
        n_results=2
    )
    print("✅ 查询成功")
    print(f"查询结果: {results}")
except Exception as e:
    print(f"❌ 查询失败: {e}")

print("\n=== 测试完成 ===")
