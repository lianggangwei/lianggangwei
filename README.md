
# ChromaDB 项目

ChromaDB 向量数据库的安装和使用项目，包含增强版工具包和便捷功能。

## 环境信息

- **操作系统**: Windows 10.0.19045
- **Python版本**: 3.14.3
- **ChromaDB版本**: 1.5.2

## 快速开始

### 1. 验证安装

```bash
python verify_chroma.py
```

### 2. 运行基础示例

```bash
python chroma_example.py
```

### 3. 运行增强版示例（推荐）

```bash
python chroma_enhanced_demo.py
```

### 4. 使用增强版工具包（推荐）

```python
from chroma_utils import KnowledgeBase, SimpleEmbeddingGenerator, batch_add_documents

# 创建知识库（支持持久化存储）
kb = KnowledgeBase(
    name="my_knowledge_base",
    persist_directory="./chroma_db",  # 可选，持久化到磁盘
    embedding_dim=128
)

# 添加文档（自动生成嵌入向量）
doc_id = kb.add_document(
    "这是一篇关于人工智能的文档",
    metadata={"category": "ai", "author": "user"}
)

# 批量添加文档
documents = [
    {"content": "文档1内容", "metadata": {"tag": "tech"}, "id": "doc1"},
    {"content": "文档2内容", "metadata": {"tag": "science"}, "id": "doc2"}
]
batch_add_documents(kb, documents, batch_size=100)

# 查询文档
results = kb.query(
    "人工智能",
    n_results=5,
    where={"category": "ai"}  # 可选过滤条件
)

# 获取所有文档
all_docs = kb.get_all_documents()

# 更新文档
kb.update_document(
    doc_id,
    document="更新后的文档内容",
    metadata={"category": "ai", "updated": True}
)

# 删除文档
kb.delete_document(doc_id)

# 获取文档数量
count = kb.count()

# 删除整个知识库
kb.delete()
```

### 5. 使用基础接口

```python
from chroma_init import init_chromadb

# 初始化（解决Python 3.14兼容性问题）
init_chromadb()

# 导入ChromaDB
import chromadb

# 创建客户端
client = chromadb.Client()

# 创建集合
collection = client.create_collection(name="my_collection")

# 添加文档（使用自定义嵌入向量）
collection.add(
    documents=["文档内容"],
    embeddings=[[0.1, 0.2, 0.3, 0.4, 0.5]],
    ids=["1"]
)

# 查询文档
results = collection.query(
    query_embeddings=[[0.15, 0.25, 0.35, 0.45, 0.55]],
    n_results=2
)
```

## 项目文件

| 文件名 | 说明 |
|--------|------|
| `chroma_utils.py` | **增强版工具包**（推荐使用），包含KnowledgeBase类、SimpleEmbeddingGenerator类等 |
| `chroma_init.py` | 基础便捷初始化模块 |
| `chroma_enhanced_demo.py` | **增强版完整示例**（推荐） |
| `chroma_example.py` | 基础使用示例 |
| `verify_chroma.py` | 安装状态验证 |
| `test_chroma_final.py` | 完整功能测试 |
| `final_status_report.md` | 详细安装报告 |

## 增强版功能

### 1. KnowledgeBase 类
- 简化的知识库管理接口
- 自动处理嵌入向量生成
- 支持持久化存储
- 支持元数据和过滤查询

### 2. SimpleEmbeddingGenerator 类
- 本地生成嵌入向量，无需网络
- 可配置向量维度
- 支持批量生成

### 3. 批量操作
- 支持大批量文档分批添加
- 避免内存溢出问题

### 4. 持久化存储
- 数据保存到磁盘
- 程序重启后数据不丢失

## 注意事项

1. **Python 3.14兼容性**: 增强版工具包已自动处理
2. **嵌入向量**: 增强版使用SimpleEmbeddingGenerator，避免网络依赖
3. **虚拟环境**: 项目使用venv虚拟环境，请确保已激活
4. **相似度说明**: SimpleEmbeddingGenerator使用简单哈希算法，实际生产建议使用专业嵌入模型

## 技术细节

### 解决的问题

1. **Python 3.14与Pydantic V1兼容性**: 通过猴子补丁替换pydantic.v1模块
2. **嵌入模型网络超时**: 使用本地嵌入生成器，不依赖网络下载

### 目录结构
- `./chroma_db/`: 持久化数据存储目录（使用持久化功能时自动创建）

## 许可证

MIT

