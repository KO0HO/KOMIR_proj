import pandas as pd

from .config import (
    DATE_COL,
    INDEX_COL,
    RETURN_COL,
    BOLLINGER_LOWER_COL,
    BOLLINGER_UPPER_COL,
    STD_COL,
    RSI_COL,
    MACD_COL,
    SIGNAL_COL,
    DISPARITY_COL,
)


def _convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = [
        INDEX_COL,
        "등락가",
        RETURN_COL,
        "이동평균(10)",
        "이동평균(20)",
        "이동평균(60)",
        "이동평균(120)",
        "이동평균(200)",
        BOLLINGER_LOWER_COL,
        BOLLINGER_UPPER_COL,
        STD_COL,
        "하한이격률",
        "상한이격률",
        "투자심리선",
        RSI_COL,
        MACD_COL,
        SIGNAL_COL,
        "이격도(10)",
        "이격도(20)",
        "이격도(60)",
        "이격도(120)",
        "이격도(200)",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("%", "", regex=False)
                .replace("nan", pd.NA)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
    df = df.dropna(subset=[DATE_COL])
    df = df.sort_values(DATE_COL).drop_duplicates(subset=[DATE_COL], keep="last").reset_index(drop=True)
    df = _convert_numeric_columns(df)

    required_cols = [
        INDEX_COL,
        RETURN_COL,
        DISPARITY_COL,
        BOLLINGER_LOWER_COL,
        BOLLINGER_UPPER_COL,
        STD_COL,
        RSI_COL,
        MACD_COL,
        SIGNAL_COL,
    ]
    required_cols = [col for col in required_cols if col in df.columns]

    df_model = df.dropna(subset=required_cols).copy()
    return df_model
