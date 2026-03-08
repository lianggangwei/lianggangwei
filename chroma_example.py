
from chroma_init import init_chromadb, get_chroma_client

init_chromadb()
import chromadb
import numpy as np

print("=== ChromaDB实用示例 ===")

# 1. 创建客户端
print("\n1. 创建客户端")
client = get_chroma_client()
print("✅ 客户端创建成功")

# 2. 创建集合
print("\n2. 创建知识集合")
collection = client.create_collection(name="knowledge_base")
print("✅ 集合创建成功")

# 3. 添加示例文档（模拟知识库）
print("\n3. 添加文档到知识库")
documents = [
    "Python是一种高级编程语言，以其简洁的语法而闻名",
    "ChromaDB是一个开源的向量数据库，用于构建AI应用",
    "机器学习是人工智能的一个分支，专注于从数据中学习",
    "向量嵌入是将文本转换为数值向量的技术",
    "Trae IDE是一个强大的AI辅助编程环境"
]

# 生成简单的嵌入向量（实际应用中应使用真实的嵌入模型）
embeddings = [
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
    [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1],
    [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1, 0.2],
    [0.5, 0.6, 0.7, 0.8, 0.9, 0.1, 0.2, 0.3]
]

ids = ["doc1", "doc2", "doc3", "doc4", "doc5"]

collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=ids
)
print("✅ 文档添加成功")

# 4. 查询文档
print("\n4. 查询文档")
query_embedding = [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85]
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

print("查询结果:")
for i, doc in enumerate(results['documents'][0]):
    distance = results['distances'][0][i]
    print(f"  {i+1}. {doc} (相似度: {1-distance:.2f})")

# 5. 获取所有文档
print("\n5. 获取所有文档")
all_docs = collection.get()
print(f"总共有 {len(all_docs['ids'])} 个文档")

# 6. 更新文档
print("\n6. 更新文档")
collection.update(
    ids=["doc1"],
    documents=["Python是一种高级编程语言，以其简洁的语法和强大的生态系统而闻名"],
    embeddings=[[0.11, 0.21, 0.31, 0.41, 0.51, 0.61, 0.71, 0.81]]
)
print("✅ 文档更新成功")

# 7. 列出所有集合
print("\n7. 列出所有集合")
collections = client.list_collections()
print(f"集合列表: {[col.name for col in collections]}")

# 8. 清理（可选）
print("\n8. 清理测试集合")
client.delete_collection(name="knowledge_base")
print("✅ 集合删除成功")

print("\n=== 示例完成 ===")
print("🎉 你已经学会了ChromaDB的基本使用！")

