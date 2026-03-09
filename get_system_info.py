import platform
import subprocess
import json
from datetime import datetime
import os


def get_cpu_info():
    try:
        result = subprocess.run(
            ['wmic', 'cpu', 'get', 'name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed', '/format:list'],
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        info = {}
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if '=' in line:
                key, value = line.split('=', 1)
                info[key.strip()] = value.strip()
        return info
    except Exception as e:
        return {'error': str(e)}


def get_gpu_info():
    try:
        result = subprocess.run(
            ['wmic', 'path', 'win32_VideoController', 'get', 'name,AdapterRAM,DriverVersion', '/format:list'],
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        gpus = []
        current_gpu = {}
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if line.strip() == '':
                if current_gpu:
                    gpus.append(current_gpu)
                    current_gpu = {}
            elif '=' in line:
                key, value = line.split('=', 1)
                current_gpu[key.strip()] = value.strip()
        if current_gpu:
            gpus.append(current_gpu)
        return gpus
    except Exception as e:
        return [{'error': str(e)}]


def get_memory_info():
    try:
        result = subprocess.run(
            ['wmic', 'memorychip', 'get', 'Capacity,Speed,Manufacturer,PartNumber', '/format:list'],
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        memory_modules = []
        current_module = {}
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if line.strip() == '':
                if current_module:
                    memory_modules.append(current_module)
                    current_module = {}
            elif '=' in line:
                key, value = line.split('=', 1)
                current_module[key.strip()] = value.strip()
        if current_module:
            memory_modules.append(current_module)
        
        total_memory = subprocess.run(
            ['wmic', 'OS', 'get', 'TotalVisibleMemorySize', '/format:list'],
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        total_info = {}
        for line in total_memory.stdout.strip().split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                total_info[key.strip()] = value.strip()
        
        return {
            'modules': memory_modules,
            'total': total_info
        }
    except Exception as e:
        return {'error': str(e)}


def get_disk_info():
    try:
        result = subprocess.run(
            ['wmic', 'diskdrive', 'get', 'Model,Size,InterfaceType', '/format:list'],
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        disks = []
        current_disk = {}
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if line.strip() == '':
                if current_disk:
                    disks.append(current_disk)
                    current_disk = {}
            elif '=' in line:
                key, value = line.split('=', 1)
                current_disk[key.strip()] = value.strip()
        if current_disk:
            disks.append(current_disk)
        
        logical_disks = subprocess.run(
            ['wmic', 'logicaldisk', 'get', 'DeviceID,VolumeName,Size,FreeSpace,FileSystem', '/format:list'],
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        logical = []
        current_logical = {}
        for line in logical_disks.stdout.strip().split('\n'):
            if line.strip() == '':
                if current_logical:
                    logical.append(current_logical)
                    current_logical = {}
            elif '=' in line:
                key, value = line.split('=', 1)
                current_logical[key.strip()] = value.strip()
        if current_logical:
            logical.append(current_logical)
        
        return {
            'physical': disks,
            'logical': logical
        }
    except Exception as e:
        return {'error': str(e)}


def get_motherboard_info():
    try:
        result = subprocess.run(
            ['wmic', 'baseboard', 'get', 'Product,Manufacturer,Version,SerialNumber', '/format:list'],
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        info = {}
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if '=' in line:
                key, value = line.split('=', 1)
                info[key.strip()] = value.strip()
        return info
    except Exception as e:
        return {'error': str(e)}


def get_system_summary():
    print("="*60)
    print("系统硬件信息获取")
    print("="*60)
    print()
    
    print("【1. CPU 信息】")
    cpu = get_cpu_info()
    print(f"  型号: {cpu.get('Name', 'N/A')}")
    print(f"  核心数: {cpu.get('NumberOfCores', 'N/A')}")
    print(f"  逻辑处理器: {cpu.get('NumberOfLogicalProcessors', 'N/A')}")
    print(f"  最大频率: {cpu.get('MaxClockSpeed', 'N/A')} MHz")
    print()
    
    print("【2. GPU 信息】")
    gpus = get_gpu_info()
    for i, gpu in enumerate(gpus, 1):
        print(f"  GPU {i}:")
        print(f"    名称: {gpu.get('Name', 'N/A')}")
        ram = gpu.get('AdapterRAM')
        if ram and ram.isdigit():
            print(f"    显存: {int(ram) / 1024 / 1024 / 1024:.2f} GB")
        else:
            print(f"    显存: {ram}")
        print(f"    驱动版本: {gpu.get('DriverVersion', 'N/A')}")
    print()
    
    print("【3. 内存 信息】")
    memory = get_memory_info()
    total = memory.get('total', {})
    total_mem = total.get('TotalVisibleMemorySize')
    if total_mem and total_mem.isdigit():
        print(f"  总内存: {int(total_mem) / 1024 / 1024:.2f} GB")
    modules = memory.get('modules', [])
    for i, mod in enumerate(modules, 1):
        print(f"  内存条 {i}:")
        capacity = mod.get('Capacity')
        if capacity and capacity.isdigit():
            print(f"    容量: {int(capacity) / 1024 / 1024 / 1024:.2f} GB")
        print(f"    厂商: {mod.get('Manufacturer', 'N/A')}")
        print(f"    频率: {mod.get('Speed', 'N/A')} MHz")
    print()
    
    print("【4. 磁盘 信息】")
    disks = get_disk_info()
    physical = disks.get('physical', [])
    for i, disk in enumerate(physical, 1):
        print(f"  物理磁盘 {i}:")
        print(f"    型号: {disk.get('Model', 'N/A')}")
        size = disk.get('Size')
        if size and size.isdigit():
            print(f"    容量: {int(size) / 1024 / 1024 / 1024:.2f} GB")
        print(f"    接口类型: {disk.get('InterfaceType', 'N/A')}")
    print()
    print("  逻辑分区:")
    logical = disks.get('logical', [])
    for ld in logical:
        drive = ld.get('DeviceID')
        if drive:
            size = ld.get('Size')
            free = ld.get('FreeSpace')
            size_str = f"{int(size) / 1024 / 1024 / 1024:.2f} GB" if size and size.isdigit() else 'N/A'
            free_str = f"{int(free) / 1024 / 1024 / 1024:.2f} GB" if free and free.isdigit() else 'N/A'
            print(f"    {drive} - {ld.get('VolumeName', 'N/A')} - {size_str} (可用: {free_str}) - {ld.get('FileSystem', 'N/A')}")
    print()
    
    print("【5. 主板 信息】")
    mb = get_motherboard_info()
    print(f"  产品: {mb.get('Product', 'N/A')}")
    print(f"  厂商: {mb.get('Manufacturer', 'N/A')}")
    print(f"  版本: {mb.get('Version', 'N/A')}")
    print()
    
    print("【6. 系统 信息】")
    print(f"  操作系统: {platform.system()} {platform.release()}")
    print(f"  计算机名: {platform.node()}")
    print(f"  处理器: {platform.processor()}")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    return {
        'timestamp': datetime.now().isoformat(),
        'cpu': cpu,
        'gpu': gpus,
        'memory': memory,
        'disk': disks,
        'motherboard': mb,
        'system': {
            'os': platform.system(),
            'release': platform.release(),
            'node': platform.node(),
            'processor': platform.processor()
        }
    }


if __name__ == "__main__":
    try:
        info = get_system_summary()
        
        filename = f"system_info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
        
        print("="*60)
        print(f"信息已保存到: {filename}")
        print("="*60)
        
    except Exception as e:
        print(f"获取信息出错: {e}")
        import traceback
        traceback.print_exc()
