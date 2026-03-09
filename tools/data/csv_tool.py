import csv
import pandas as pd
from typing import List, Dict, Any, Optional, Callable
import os


class CSVTool:
    def __init__(self, filepath: str = None, encoding: str = 'utf-8-sig'):
        self.filepath = filepath
        self.encoding = encoding

    def read(self, delimiter: str = ',') -> pd.DataFrame:
        return pd.read_csv(self.filepath, delimiter=delimiter, encoding=self.encoding)

    def read_rows(self) -> List[Dict]:
        with open(self.filepath, 'r', encoding=self.encoding, newline='') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def write(self, data: pd.DataFrame, index: bool = False):
        data.to_csv(self.filepath, index=index, encoding=self.encoding)

    def write_rows(self, rows: List[Dict], fieldnames: List[str] = None):
        if not rows:
            return
        if not fieldnames:
            fieldnames = list(rows[0].keys())
        with open(self.filepath, 'w', encoding=self.encoding, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def append_row(self, row: Dict):
        file_exists = os.path.exists(self.filepath)
        fieldnames = list(row.keys())
        mode = 'a' if file_exists else 'w'
        with open(self.filepath, mode, encoding=self.encoding, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)

    def filter(self, condition: Callable[[Dict], bool]) -> List[Dict]:
        rows = self.read_rows()
        return [row for row in rows if condition(row)]

    def transform(self, transformer: Callable[[Dict], Dict]) -> List[Dict]:
        rows = self.read_rows()
        return [transformer(row.copy()) for row in rows]

    def get_column(self, column_name: str) -> List[Any]:
        df = self.read()
        return df[column_name].tolist()

    def add_column(self, column_name: str, values: List[Any]):
        df = self.read()
        df[column_name] = values
        self.write(df)

    def drop_column(self, column_name: str):
        df = self.read()
        df = df.drop(columns=[column_name])
        self.write(df)

    def sort_by(self, column_name: str, ascending: bool = True):
        df = self.read()
        df = df.sort_values(by=column_name, ascending=ascending)
        self.write(df)
        return df

    def group_by(self, column_name: str, agg_dict: Dict[str, str] = None) -> pd.DataFrame:
        df = self.read()
        if agg_dict:
            return df.groupby(column_name).agg(agg_dict).reset_index()
        return df.groupby(column_name).size().reset_index(name='count')


def merge_csv_files(file_paths: List[str], output_path: str, encoding: str = 'utf-8-sig'):
    dfs = []
    for path in file_paths:
        df = pd.read_csv(path, encoding=encoding)
        dfs.append(df)
    merged = pd.concat(dfs, ignore_index=True)
    merged.to_csv(output_path, index=False, encoding=encoding)
    return merged


def split_csv_by_column(input_path: str, column_name: str, output_dir: str, encoding: str = 'utf-8-sig'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    df = pd.read_csv(input_path, encoding=encoding)
    groups = df.groupby(column_name)
    for name, group in groups:
        safe_name = str(name).replace('/', '_').replace('\\', '_')
        output_path = os.path.join(output_dir, f"{safe_name}.csv")
        group.to_csv(output_path, index=False, encoding=encoding)
    return list(groups.groups.keys())
