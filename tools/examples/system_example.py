import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from system.file_ops import FileManager
from system.backup import BackupTool, auto_backup


def example_file_manager():
    print("=== 文件管理示例 ===")
    fm = FileManager('.')
    py_files = fm.list_files('*.py', recursive=True)
    print(f"找到 {len(py_files)} 个Python文件")
    first_file = py_files[0] if py_files else None
    if first_file:
        info = fm.get_file_info(first_file)
        print(f"第一个文件信息:")
        print(f"  名称: {info['name']}")
        print(f"  大小: {info['size']} 字节")
        print(f"  修改时间: {info['modified']}")
    print()


def example_backup():
    print("=== 备份工具示例 ===")
    source_dir = '.'
    backup_tool = BackupTool(source_dir, backup_dir='test_backups')
    print("正在创建ZIP备份...")
    zip_backup = backup_tool.backup_to_zip(
        exclude_patterns=['venv', '.git', '__pycache__'],
        prefix='my_project'
    )
    print(f"备份已创建: {zip_backup}")
    size = backup_tool.get_backup_size(zip_backup)
    print(f"备份大小: {size / 1024:.2f} KB")
    backups = backup_tool.list_backups()
    print(f"共有 {len(backups)} 个备份")
    print()


def example_auto_backup():
    print("=== 自动备份示例 ===")
    print("这是一个简单的自动备份函数，可以定期调用")
    print("使用示例:")
    print("  auto_backup('.', format='zip', keep_count=5)")
    print()


if __name__ == "__main__":
    try:
        example_file_manager()
        example_auto_backup()
        print("所有系统工具示例运行完成！")
    except Exception as e:
        print(f"示例运行出错: {e}")
