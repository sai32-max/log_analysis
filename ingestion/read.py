import gzip
import logging
import os
import os.path as pt

logger = logging.getLogger(__name__)


def ingest(path: str):
    rows = []
    for file in os.listdir(path):
        file_path = pt.join(path, file)
        try:
            with open(file_path, 'rb') as probe:
                is_gzip = probe.read(2) == b'\x1f\x8b'
            if is_gzip:
                opener = gzip.open(file_path, mode='rt', encoding='utf-8', errors='replace')
            else:
                opener = open(file_path, encoding='utf-8', errors='replace')
            with opener as f:
                rows.extend(f.readlines())
        except Exception:
            logger.exception("Impossible de lire le fichier %s", file)
    return rows