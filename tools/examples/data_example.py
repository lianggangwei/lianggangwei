import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from data.excel import ExcelTool
from data.csv_tool import CSVTool
from data.database import SQLiteTool


def example_excel_tool():
    print("=== Excel工具示例 ===")
    excel = ExcelTool('example.xlsx')
    data = pd.DataFrame({
        '姓名': ['张三', '李四', '王五'],
        '年龄': [25, 30, 35],
        '城市': ['北京', '上海', '广州']
    })
    excel.write_excel(data, sheet_name='人员信息')
    excel.format_header('人员信息')
    excel.append_row('人员信息', ['赵六', 28, '深圳'])
    print("Excel文件已创建: example.xlsx")
    df = excel.read_sheet('人员信息')
    print(f"读取的数据:\n{df}")
    print()


def example_csv_tool():
    print("=== CSV工具示例 ===")
    csv_tool = CSVTool('example.csv')
    data = pd.DataFrame({
        '产品': ['A', 'B', 'C', 'A', 'B'],
        '销量': [100, 200, 150, 120, 180],
        '月份': ['1月', '1月', '1月', '2月', '2月']
    })
    csv_tool.write(data)
    print("CSV文件已创建: example.csv")
    df = csv_tool.read()
    print(f"读取的数据:\n{df}")
    grouped = csv_tool.group_by('产品', {'销量': 'sum'})
    print(f"按产品分组统计:\n{grouped}")
    print()


def example_database():
    print("=== SQLite数据库示例 ===")
    with SQLiteTool('example.db') as db:
        db.create_table('users', {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'name': 'TEXT',
            'email': 'TEXT',
            'age': 'INTEGER'
        })
        db.insert('users', {'name': '张三', 'email': 'zhang@example.com', 'age': 25})
        db.insert('users', {'name': '李四', 'email': 'li@example.com', 'age': 30})
        users = db.query('SELECT * FROM users')
        print(f"数据库中的用户: {users}")
        df = db.query_to_df('SELECT * FROM users')
        print(f"DataFrame格式:\n{df}")
    print()


if __name__ == "__main__":
    try:
        example_excel_tool()
        example_csv_tool()
        example_database()
        print("所有数据处理示例运行完成！")
    except Exception as e:
        print(f"示例运行出错: {e}")
