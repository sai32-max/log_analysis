import gzip
import os
import os.path as pt


def ingest(path: str):
    rows = []
    try:
        for file in os.listdir(path):
            file_path = pt.join(path, file)
            if file.endswith('.gz'):
                opener = gzip.open(file_path, mode='rt', encoding='utf-8')
            else:
                opener = open(file_path, encoding='utf-8')
            with opener as f:
                rows.extend(f.readlines())
    except Exception as e:
        print(e)
        return None
    return rows


if __name__ == "__main__":
    data = ingest('./data')
    if data:
        print(len(data), "lignes lues")