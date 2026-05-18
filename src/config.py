from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
RESULT_DIR = ROOT_DIR / "result"

RAW_FILE = "한국광해광업공단_파생지수_광물종합지수.csv"

RESULT_FULL = "mineral_composite_index_anomaly_detection_full_result.csv"
RESULT_LIST = "mineral_composite_index_anomaly_list.csv"

# 컬럼명
DATE_COL = "기준일"
INDEX_COL = "광물종합지수(2016년1월 1000인지수)"
RETURN_COL = "등락율(퍼센트)"
MA20_COL = "이동평균(20)"
MA60_COL = "이동평균(60)"
BOLLINGER_LOWER_COL = "볼린저밴드(하한선)"
BOLLINGER_MID_COL = "볼린저밴드(중심선)"
BOLLINGER_UPPER_COL = "볼린저밴드(상한선)"
STD_COL = "표준편차(20)"
DISPARITY_COL = "이격도(20)"
RSI_COL = "상대강도지수(RSI)"
MACD_COL = "이동평균 수렴확산(MACD)"
SIGNAL_COL = "시그널"

# 임계값
Z_THRESHOLD = 3.0
DISPARITY_UPPER_THRESHOLD = 115
DISPARITY_LOWER_THRESHOLD = 85
VOLATILITY_Z_THRESHOLD = 2.5
MA_DISPARITY_MARGIN = 0.05
BOLLINGER_MARGIN = 0.02
RSI_OVERBOUGHT = 90
RSI_OVERSOLD = 10
RSI_RETURN_ZSCORE_THRESHOLD = 1.5
CONTAMINATION_RATE = 0.01
