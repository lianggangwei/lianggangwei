import os
import sys

# 设置环境变量以禁用Pydantic警告
os.environ['PYDANTIC_DISABLE_VALIDATORS'] = '1'

print("=== 测试ChromaDB基本功能（带环境变量）===")

try:
    import chromadb
    print("1. 测试导入:")
    print(f"ChromaDB版本: {chromadb.__version__}")
    
    # 2. 测试创建客户端
    print("\n2. 测试创建客户端:")
    client = chromadb.Client()
    print("✅ 客户端创建成功")
    
    # 3. 测试创建集合
    print("\n3. 测试创建集合:")
    collection = client.create_collection(name="test_collection")
    print("✅ 集合创建成功")
    
    # 4. 测试添加文档
    print("\n4. 测试添加文档:")
    collection.add(
        documents=["这是第一个文档", "这是第二个文档", "这是第三个文档"],
        ids=["1", "2", "3"]
    )
    print("✅ 文档添加成功")
    
    # 5. 测试查询
    print("\n5. 测试查询:")
    results = collection.query(
        query_texts=["第一个"],
        n_results=2
    )
    print("✅ 查询成功")
    print(f"查询结果: {results}")
    
    print("\n=== 测试完成 ===")
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
