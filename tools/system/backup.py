import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import List, Optional
import tarfile


class BackupTool:
    def __init__(self, source_dir: str, backup_dir: str = 'backups'):
        self.source_dir = Path(source_dir).resolve()
        self.backup_dir = Path(backup_dir).resolve()
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup_name(self, prefix: str = 'backup') -> str:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{prefix}_{timestamp}"

    def backup_to_zip(self, include_patterns: List[str] = None,
                      exclude_patterns: List[str] = None,
                      prefix: str = 'backup') -> str:
        backup_name = self.create_backup_name(prefix)
        zip_path = self.backup_dir / f"{backup_name}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.source_dir):
                for file in files:
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(self.source_dir)
                    if self._should_include(rel_path, include_patterns, exclude_patterns):
                        zipf.write(file_path, rel_path)
        return str(zip_path)

    def backup_to_tar(self, include_patterns: List[str] = None,
                     exclude_patterns: List[str] = None,
                     prefix: str = 'backup',
                     compression: str = 'gz') -> str:
        backup_name = self.create_backup_name(prefix)
        ext = f".tar.{compression}" if compression else ".tar"
        tar_path = self.backup_dir / f"{backup_name}{ext}"
        mode = f'w:{compression}' if compression else 'w'
        with tarfile.open(tar_path, mode) as tar:
            for root, dirs, files in os.walk(self.source_dir):
                for file in files:
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(self.source_dir)
                    if self._should_include(rel_path, include_patterns, exclude_patterns):
                        tar.add(file_path, rel_path)
        return str(tar_path)

    def backup_to_directory(self, include_patterns: List[str] = None,
                           exclude_patterns: List[str] = None,
                           prefix: str = 'backup') -> str:
        backup_name = self.create_backup_name(prefix)
        dest_dir = self.backup_dir / backup_name
        dest_dir.mkdir(parents=True, exist_ok=True)
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                src_path = Path(root) / file
                rel_path = src_path.relative_to(self.source_dir)
                if self._should_include(rel_path, include_patterns, exclude_patterns):
                    dest_path = dest_dir / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_path, dest_path)
        return str(dest_dir)

    def _should_include(self, path: Path, include_patterns: List[str] = None,
                       exclude_patterns: List[str] = None) -> bool:
        path_str = str(path)
        if exclude_patterns:
            for pattern in exclude_patterns:
                if pattern in path_str:
                    return False
        if include_patterns:
            for pattern in include_patterns:
                if pattern in path_str:
                    return True
            return False
        return True

    def list_backups(self) -> List[Path]:
        return sorted(self.backup_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)

    def restore_backup(self, backup_path: str, dest_dir: str = None):
        backup_file = Path(backup_path)
        if not backup_file.exists():
            raise FileNotFoundError(f"备份文件不存在: {backup_path}")
        dest = Path(dest_dir) if dest_dir else self.source_dir
        dest.mkdir(parents=True, exist_ok=True)
        if backup_file.suffix == '.zip':
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall(dest)
        elif backup_file.suffixes[:2] == ['.tar', '.gz'] or backup_file.suffix == '.tar':
            with tarfile.open(backup_file, 'r:*') as tar:
                tar.extractall(dest)
        else:
            raise ValueError(f"不支持的备份格式: {backup_file.suffix}")

    def delete_old_backups(self, keep_count: int = 10):
        backups = self.list_backups()
        for backup in backups[keep_count:]:
            if backup.is_file():
                backup.unlink()
            elif backup.is_dir():
                shutil.rmtree(backup)

    def get_backup_size(self, backup_path: str) -> int:
        backup = Path(backup_path)
        if backup.is_file():
            return backup.stat().st_size
        elif backup.is_dir():
            total = 0
            for f in backup.rglob('*'):
                if f.is_file():
                    total += f.stat().st_size
            return total
        return 0


def auto_backup(source_dir: str, backup_dir: str = 'backups',
                format: str = 'zip', keep_count: int = 10, **kwargs) -> str:
    tool = BackupTool(source_dir, backup_dir)
    if format == 'zip':
        backup_path = tool.backup_to_zip(**kwargs)
    elif format == 'tar':
        backup_path = tool.backup_to_tar(**kwargs)
    else:
        backup_path = tool.backup_to_directory(**kwargs)
    tool.delete_old_backups(keep_count)
    return backup_path
