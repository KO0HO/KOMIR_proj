from pathlib import Path
import pandas as pd

from .config import DATA_DIR, RAW_FILE


def load_raw_data(file_name: str = RAW_FILE, encoding: str = "cp949") -> pd.DataFrame:
    file_path = Path(DATA_DIR) / file_name
    df = pd.read_csv(file_path, encoding=encoding)
    return df
