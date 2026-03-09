import os
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
import hashlib
from datetime import datetime


class FileManager:
    def __init__(self, base_path: str = '.'):
        self.base_path = Path(base_path).resolve()

    def list_files(self, pattern: str = '*', recursive: bool = False) -> List[Path]:
        if recursive:
            return list(self.base_path.rglob(pattern))
        return list(self.base_path.glob(pattern))

    def find_files(self, name_contains: str = None, extension: str = None,
                   min_size: int = None, max_size: int = None) -> List[Path]:
        results = []
        for file in self.base_path.rglob('*'):
            if file.is_file():
                if name_contains and name_contains not in file.name:
                    continue
                if extension and not file.suffix == extension:
                    continue
                size = file.stat().st_size
                if min_size is not None and size < min_size:
                    continue
                if max_size is not None and size > max_size:
                    continue
                results.append(file)
        return results

    def copy_file(self, src: str, dst: str, overwrite: bool = False):
        src_path = Path(src)
        dst_path = Path(dst)
        if not src_path.exists():
            raise FileNotFoundError(f"源文件不存在: {src}")
        if dst_path.exists() and not overwrite:
            raise FileExistsError(f"目标文件已存在: {dst}")
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)

    def move_file(self, src: str, dst: str, overwrite: bool = False):
        src_path = Path(src)
        dst_path = Path(dst)
        if not src_path.exists():
            raise FileNotFoundError(f"源文件不存在: {src}")
        if dst_path.exists() and not overwrite:
            raise FileExistsError(f"目标文件已存在: {dst}")
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(src_path, dst_path)

    def delete_file(self, path: str):
        file_path = Path(path)
        if file_path.exists() and file_path.is_file():
            file_path.unlink()

    def delete_directory(self, path: str, force: bool = False):
        dir_path = Path(path)
        if dir_path.exists() and dir_path.is_dir():
            if force:
                shutil.rmtree(dir_path)
            else:
                dir_path.rmdir()

    def get_file_hash(self, path: str, algorithm: str = 'md5') -> str:
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {path}")
        hash_obj = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()

    def find_duplicates(self, directory: str = None) -> Dict[str, List[Path]]:
        search_path = Path(directory) if directory else self.base_path
        hash_map = {}
        for file in search_path.rglob('*'):
            if file.is_file():
                file_hash = self.get_file_hash(file)
                if file_hash not in hash_map:
                    hash_map[file_hash] = []
                hash_map[file_hash].append(file)
        return {k: v for k, v in hash_map.items() if len(v) > 1}

    def batch_rename(self, directory: str, pattern: str, replacement: str):
        dir_path = Path(directory)
        count = 0
        for file in dir_path.iterdir():
            if file.is_file():
                new_name = file.name.replace(pattern, replacement)
                if new_name != file.name:
                    new_path = file.parent / new_name
                    file.rename(new_path)
                    count += 1
        return count

    def get_file_info(self, path: str) -> Dict[str, Any]:
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {path}")
        stat = file_path.stat()
        return {
            'path': str(file_path),
            'name': file_path.name,
            'size': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'is_file': file_path.is_file(),
            'is_dir': file_path.is_dir()
        }
