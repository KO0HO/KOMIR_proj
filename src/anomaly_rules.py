from typing import List

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from .config import (
    BOLLINGER_MARGIN,
    CONTAMINATION_RATE,
    DISPARITY_LOWER_THRESHOLD,
    DISPARITY_UPPER_THRESHOLD,
    MA20_COL,
    MA_DISPARITY_MARGIN,
    BOLLINGER_LOWER_COL,
    BOLLINGER_UPPER_COL,
    DATE_COL,
    DISPARITY_COL,
    INDEX_COL,
    MACD_COL,
    RETURN_COL,
    RSI_COL,
    RSI_RETURN_ZSCORE_THRESHOLD,
    SIGNAL_COL,
    STD_COL,
    Z_THRESHOLD,
    VOLATILITY_Z_THRESHOLD,
    RSI_OVERBOUGHT,
    RSI_OVERSOLD,
)


def _assign_anomaly_grade(score: float) -> str:
    if score <= 1:
        return "정상"
    elif score <= 2:
        return "주의"
    elif score <= 3:
        return "경계"
    return "심각"


def _make_reason(row: pd.Series) -> str:
    reasons: List[str] = []

    if row.get("flag_return_zscore", 0) == 1:
        reasons.append("등락율 급등락")
    if row.get("flag_disparity", 0) == 1:
        reasons.append("이동평균 대비 과도한 이탈")
    if row.get("flag_bollinger_upper", 0) == 1:
        reasons.append("볼린저밴드 상단 이탈")
    if row.get("flag_bollinger_lower", 0) == 1:
        reasons.append("볼린저밴드 하단 이탈")
    if row.get("flag_volatility", 0) == 1:
        reasons.append("변동성 확대")
    if row.get("flag_rsi_overbought", 0) == 1:
        reasons.append("RSI 과매수 구간")
    if row.get("flag_rsi_oversold", 0) == 1:
        reasons.append("RSI 과매도 구간")
    if row.get("flag_macd_golden_cross", 0) == 1:
        reasons.append("MACD 골든크로스")
    if row.get("flag_macd_dead_cross", 0) == 1:
        reasons.append("MACD 데드크로스")
    if row.get("flag_isolation_forest", 0) == 1:
        reasons.append("Isolation Forest 이상치")

    if not reasons:
        return "정상 범위"
    return ", ".join(reasons)


def apply_anomaly_detection(df_model: pd.DataFrame) -> pd.DataFrame:
    df = df_model.copy()

    if RETURN_COL in df.columns:
        return_mean = df[RETURN_COL].mean()
        return_std = df[RETURN_COL].std()
        df["return_zscore"] = (df[RETURN_COL] - return_mean) / return_std
        df["flag_return_zscore"] = (df["return_zscore"].abs() >= Z_THRESHOLD).astype(int)

    if MA20_COL in df.columns and INDEX_COL in df.columns:
        df["ma20_gap_ratio"] = (df[INDEX_COL] - df[MA20_COL]).abs() / df[MA20_COL]
    else:
        df["ma20_gap_ratio"] = 0.0

    if DISPARITY_COL in df.columns:
        df["flag_disparity"] = (
            (
                (df[DISPARITY_COL] >= DISPARITY_UPPER_THRESHOLD) |
                (df[DISPARITY_COL] <= DISPARITY_LOWER_THRESHOLD)
            ) &
            (df["ma20_gap_ratio"] >= MA_DISPARITY_MARGIN)
        ).astype(int)

    if all(col in df.columns for col in [INDEX_COL, BOLLINGER_UPPER_COL]):
        df["flag_bollinger_upper"] = (
            df[INDEX_COL] > (1 + BOLLINGER_MARGIN) * df[BOLLINGER_UPPER_COL]
        ).astype(int)
    if all(col in df.columns for col in [INDEX_COL, BOLLINGER_LOWER_COL]):
        df["flag_bollinger_lower"] = (
            df[INDEX_COL] < (1 - BOLLINGER_MARGIN) * df[BOLLINGER_LOWER_COL]
        ).astype(int)
    df["flag_bollinger"] = (
        (df.get("flag_bollinger_upper", 0) == 1) |
        (df.get("flag_bollinger_lower", 0) == 1)
    ).astype(int)

    if STD_COL in df.columns:
        vol_mean = df[STD_COL].mean()
        vol_std = df[STD_COL].std()
        df["volatility_zscore"] = (df[STD_COL] - vol_mean) / vol_std
        df["flag_volatility"] = (df["volatility_zscore"] >= VOLATILITY_Z_THRESHOLD).astype(int)

    if RSI_COL in df.columns:
        if RETURN_COL in df.columns:
            df["flag_rsi_overbought"] = (
                (df[RSI_COL] >= RSI_OVERBOUGHT) &
                (df["return_zscore"] >= RSI_RETURN_ZSCORE_THRESHOLD)
            ).astype(int)
            df["flag_rsi_oversold"] = (
                (df[RSI_COL] <= RSI_OVERSOLD) &
                (df["return_zscore"] <= -RSI_RETURN_ZSCORE_THRESHOLD)
            ).astype(int)
        else:
            df["flag_rsi_overbought"] = (df[RSI_COL] >= RSI_OVERBOUGHT).astype(int)
            df["flag_rsi_oversold"] = (df[RSI_COL] <= RSI_OVERSOLD).astype(int)
        df["flag_rsi"] = ((df["flag_rsi_overbought"] == 1) | (df["flag_rsi_oversold"] == 1)).astype(int)

    if all(col in df.columns for col in [MACD_COL, SIGNAL_COL]):
        df["macd_diff"] = df[MACD_COL] - df[SIGNAL_COL]
        df["macd_diff_prev"] = df["macd_diff"].shift(1)
        df["flag_macd_golden_cross"] = (
            (df["macd_diff_prev"] < 0) & (df["macd_diff"] > 0)
        ).astype(int)
        df["flag_macd_dead_cross"] = (
            (df["macd_diff_prev"] > 0) & (df["macd_diff"] < 0)
        ).astype(int)
        df["flag_macd"] = ((df["flag_macd_golden_cross"] == 1) | (df["flag_macd_dead_cross"] == 1)).astype(int)

    if_features = [
        INDEX_COL,
        RETURN_COL,
        DISPARITY_COL,
        STD_COL,
        RSI_COL,
        MACD_COL,
        SIGNAL_COL,
    ]
    if_features = [col for col in if_features if col in df.columns]

    if if_features:
        X = df[if_features].copy()
        X = X.fillna(X.median(numeric_only=True))
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        iso_model = IsolationForest(
            n_estimators=300,
            contamination=CONTAMINATION_RATE,
            random_state=42,
        )
        df["isolation_result"] = iso_model.fit_predict(X_scaled)
        df["flag_isolation_forest"] = (df["isolation_result"] == -1).astype(int)
        df["isolation_score"] = iso_model.decision_function(X_scaled)
    else:
        df["flag_isolation_forest"] = 0

    flag_cols = [
        "flag_return_zscore",
        "flag_disparity",
        "flag_bollinger",
        "flag_volatility",
        "flag_rsi",
        "flag_macd",
        "flag_isolation_forest",
    ]
    flag_cols = [col for col in flag_cols if col in df.columns]
    df["anomaly_score"] = df[flag_cols].sum(axis=1)
    df["이상등급"] = df["anomaly_score"].apply(_assign_anomaly_grade)
    df["탐지사유"] = df.apply(_make_reason, axis=1)

    return df


def build_anomaly_list(df_model: pd.DataFrame) -> pd.DataFrame:
    output_cols = [
        DATE_COL,
        INDEX_COL,
        RETURN_COL,
        "anomaly_score",
        "이상등급",
        "탐지사유",
    ]
    available_cols = [col for col in output_cols if col in df_model.columns]
    anomaly_list = df_model[df_model["이상등급"] != "정상"].copy()
    anomaly_list = anomaly_list[available_cols].sort_values(DATE_COL)
    anomaly_list = anomaly_list.rename(columns={
        DATE_COL: "Date",
        INDEX_COL: "Mineral Composite Index",
        RETURN_COL: "Return Rate (%)",
        "anomaly_score": "Anomaly Score",
        "이상등급": "Anomaly Grade",
        "탐지사유": "Detection Reason",
    })
    return anomaly_list
