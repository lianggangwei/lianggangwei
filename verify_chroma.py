
from chroma_init import init_chromadb

print("=== ChromaDB安装状态验证 ===")

try:
    # 1. 测试初始化
    print("1. 测试初始化...")
    init_chromadb()
    print("✅ 初始化成功")
    
    # 2. 测试导入
    print("\n2. 测试导入...")
    import chromadb
    print(f"✅ 导入成功，版本: {chromadb.__version__}")
    
    # 3. 测试创建客户端
    print("\n3. 测试创建客户端...")
    client = chromadb.Client()
    print("✅ 客户端创建成功")
    
    # 4. 测试创建简单集合
    print("\n4. 测试创建集合...")
    collection = client.create_collection(name="quick_check")
    print("✅ 集合创建成功")
    
    # 5. 清理
    print("\n5. 清理测试集合...")
    client.delete_collection(name="quick_check")
    print("✅ 清理成功")
    
    print("\n=== 验证完成 ===")
    print("🎉 ChromaDB安装和配置正常！")
    print("\n可用文件:")
    print("  - chroma_init.py: 便捷初始化模块")
    print("  - chroma_example.py: 完整使用示例")
    print("  - test_chroma_final.py: 完整功能测试")
    
except Exception as e:
    print(f"\n❌ 验证失败: {e}")
    import traceback
    traceback.print_exc()

