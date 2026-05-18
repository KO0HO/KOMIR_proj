from datetime import datetime
from pathlib import Path
import pandas as pd

from .config import RESULT_DIR, RESULT_FULL, RESULT_LIST


def save_results(df_model: pd.DataFrame, anomaly_list: pd.DataFrame) -> dict:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    full_path = RESULT_DIR / f"{Path(RESULT_FULL).stem}_{timestamp}{Path(RESULT_FULL).suffix}"
    list_path = RESULT_DIR / f"{Path(RESULT_LIST).stem}_{timestamp}{Path(RESULT_LIST).suffix}"
    df_model.to_csv(full_path, index=False)
    anomaly_list.to_csv(list_path, index=False)
    return {
        "full": full_path,
        "list": list_path,
        "timestamp": timestamp,
    }
