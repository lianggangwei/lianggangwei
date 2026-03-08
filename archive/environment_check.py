import os
import sys
import platform
import subprocess
import json

# 检测操作系统信息
def check_os():
    return {
        "name": platform.system(),
        "version": platform.version(),
        "arch": platform.architecture()[0],
        "machine": platform.machine(),
        "node": platform.node()
    }

# 检测Python环境
def check_python():
    return {
        "version": platform.python_version(),
        "implementation": platform.python_implementation(),
        "path": sys.executable,
        "sys_path": sys.path,
        "pip_version": subprocess.getoutput("pip --version").split()[1] if sys.platform == "win32" else subprocess.getoutput("pip3 --version").split()[1]
    }

# 检测已安装的Python包
def check_installed_packages():
    try:
        result = subprocess.check_output([sys.executable, "-m", "pip", "list", "--format=json"], text=True)
        return json.loads(result)
    except Exception as e:
        return []

# 检测开发工具和插件
def check_development_tools():
    tools = {
        "git": False,
        "node": False,
        "npm": False,
        "yarn": False,
        "docker": False
    }
    
    for tool in tools:
        try:
            if sys.platform == "win32":
                subprocess.check_output([tool, "--version"], stderr=subprocess.STDOUT, text=True)
            else:
                subprocess.check_output([tool, "--version"], stderr=subprocess.STDOUT, text=True)
            tools[tool] = True
        except:
            pass
    
    return tools

# 检测IDE环境
def check_ide():
    return {
        "ide": "Trae IDE",
        "working_directory": os.getcwd()
    }

# 主函数
def main():
    print("=== 环境检测报告 ===")
    print()
    
    # 检测操作系统
    os_info = check_os()
    print("1. 操作系统信息:")
    for key, value in os_info.items():
        print(f"   {key}: {value}")
    print()
    
    # 检测Python环境
    python_info = check_python()
    print("2. Python环境:")
    for key, value in python_info.items():
        if key == "sys_path":
            print("   sys_path:")
            for path in value[:5]:  # 只显示前5个路径
                print(f"     - {path}")
            if len(value) > 5:
                print(f"     ... 等 {len(value) - 5} 个路径")
        else:
            print(f"   {key}: {value}")
    print()
    
    # 检测已安装的Python包
    packages = check_installed_packages()
    print(f"3. 已安装的Python包 ({len(packages)} 个):")
    for package in packages[:10]:  # 只显示前10个包
        print(f"   - {package['name']}: {package['version']}")
    if len(packages) > 10:
        print(f"   ... 等 {len(packages) - 10} 个包")
    print()
    
    # 检测开发工具和插件
    tools = check_development_tools()
    print("4. 开发工具状态:")
    for tool, installed in tools.items():
        status = "已安装" if installed else "未安装"
        print(f"   {tool}: {status}")
    print()
    
    # 检测IDE环境
    ide_info = check_ide()
    print("5. IDE环境:")
    for key, value in ide_info.items():
        print(f"   {key}: {value}")
    print()
    
    # 生成环境检测报告
    report = {
        "os": os_info,
        "python": python_info,
        "packages": packages,
        "tools": tools,
        "ide": ide_info
    }
    
    # 保存报告到文件
    with open("environment_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("环境检测报告已保存到 environment_report.json")

if __name__ == "__main__":
    main()