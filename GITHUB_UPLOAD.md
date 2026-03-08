https://gitee.com/lianggangwei/lianggangwei.git
# 上传项目到 GitHub 指南

## 前置条件

1. 安装 Git: https://git-scm.com/downloads
2. 拥有 GitHub 账户: https://github.com

## 步骤

### 1. 安装 Git（如果尚未安装）

下载并安装 Git: https://git-scm.com/download/win

安装完成后，重启终端，验证安装：
```bash
git --version
```

### 2. 初始化 Git 仓库

在项目目录中运行：
```bash
git init
```

### 3. 配置 Git 用户信息

```bash
git config user.name "你的用户名"
git config user.email "你的邮箱@example.com"
```

### 4. 添加文件到 Git

```bash
git add .
```

### 5. 创建第一次提交

```bash
git commit -m "Initial commit: ChromaDB project with enhanced tools"
```

### 6. 在 GitHub 上创建新仓库

1. 访问 https://github.com/new
2. 输入仓库名称（例如：chromadb-project）
3. 选择 Public 或 Private
4. **不要**勾选 "Initialize this repository with a README"
5. 点击 "Create repository"

### 7. 连接本地仓库到 GitHub

复制 GitHub 上显示的命令，类似：
```bash
git remote add origin https://github.com/你的用户名/仓库名.git
git branch -M main
git push -u origin main
```

### 8. 后续更新

每次修改后：
```bash
git add .
git commit -m "描述你的修改"
git push
```

## 项目结构

```
chromadb-project/
├── .gitignore              # Git 忽略文件配置
├── README.md               # 项目说明文档
├── chroma_utils.py         # 增强版工具包
├── chroma_init.py          # 基础初始化模块
├── chroma_enhanced_demo.py # 完整功能演示
├── chroma_example.py       # 基础使用示例
├── verify_chroma.py        # 安装验证脚本
└── (其他测试文件...)
```

## 注意事项

- `chroma_db/` 目录（持久化数据）已在 .gitignore 中，不会被上传
- `venv/` 虚拟环境目录不会被上传
- 敏感信息不要提交到仓库

## 许可证

MIT

