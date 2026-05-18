import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from pathlib import Path
from typing import Optional

from .config import (
    DATE_COL,
    INDEX_COL,
    MA20_COL,
    MA60_COL,
    BOLLINGER_LOWER_COL,
    BOLLINGER_UPPER_COL,
    RETURN_COL,
    STD_COL,
)


def _set_korean_font() -> None:
    project_root = Path(__file__).resolve().parents[1]
    font_dir = project_root / "fonts"
    local_font = font_dir / "NanumGothic.ttf"

    if local_font.exists():
        fm.fontManager.addfont(str(local_font))

    preferred_fonts = [
        "NanumGothic",
        "Malgun Gothic",
        "NanumGothicCoding",
        "AppleGothic",
        "DejaVu Sans",
    ]
    available_fonts = {font.name for font in fm.fontManager.ttflist}

    for font_name in preferred_fonts:
        if font_name in available_fonts:
            plt.rcParams["font.family"] = font_name
            break
    else:
        plt.rcParams["font.family"] = "DejaVu Sans"

    plt.rcParams["axes.unicode_minus"] = False


_set_korean_font()


def plot_index_with_bands(df, save_path: Optional[Path] = None):
    plt.figure(figsize=(18, 8))
    plt.plot(df[DATE_COL], df[INDEX_COL], label="광물종합지수", linewidth=1.8)

    if MA20_COL in df.columns:
        plt.plot(df[DATE_COL], df[MA20_COL], label="이동평균(20)", linewidth=1.3, linestyle="--")
    if MA60_COL in df.columns:
        plt.plot(df[DATE_COL], df[MA60_COL], label="이동평균(60)", linewidth=1.3, linestyle="--")
    if BOLLINGER_UPPER_COL in df.columns:
        plt.plot(df[DATE_COL], df[BOLLINGER_UPPER_COL], label="볼린저밴드 상한선", linewidth=1, linestyle=":")
    if BOLLINGER_LOWER_COL in df.columns:
        plt.plot(df[DATE_COL], df[BOLLINGER_LOWER_COL], label="볼린저밴드 하한선", linewidth=1, linestyle=":")

    anomaly_points = df[df["이상등급"] != "정상"]
    if not anomaly_points.empty:
        plt.scatter(anomaly_points[DATE_COL], anomaly_points[INDEX_COL], s=45, label="이상징후", marker="o")

    plt.title("광물종합지수 이상징후 탐지 결과", fontsize=16)
    plt.xlabel("기준일")
    plt.ylabel("광물종합지수")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()


def plot_anomaly_grade(df, save_path: Optional[Path] = None):
    plt.figure(figsize=(18, 8))
    plt.plot(df[DATE_COL], df[INDEX_COL], label="광물종합지수", linewidth=1.8)
    if MA20_COL in df.columns:
        plt.plot(df[DATE_COL], df[MA20_COL], label="이동평균(20)", linewidth=1.2, linestyle="--")
    if BOLLINGER_UPPER_COL in df.columns:
        plt.plot(df[DATE_COL], df[BOLLINGER_UPPER_COL], label="볼린저밴드 상한선", linewidth=1, linestyle=":")
    if BOLLINGER_LOWER_COL in df.columns:
        plt.plot(df[DATE_COL], df[BOLLINGER_LOWER_COL], label="볼린저밴드 하한선", linewidth=1, linestyle=":")

    grade_marker_info = {
        "주의": {"marker": "o", "size": 40},
        "경계": {"marker": "^", "size": 70},
        "심각": {"marker": "X", "size": 100},
    }

    for grade, info in grade_marker_info.items():
        temp = df[df["이상등급"] == grade]
        if not temp.empty:
            plt.scatter(temp[DATE_COL], temp[INDEX_COL], s=info["size"], marker=info["marker"], label=f"{grade} 이상징후")

    plt.title("광물종합지수 이상등급별 탐지 결과", fontsize=16)
    plt.xlabel("기준일")
    plt.ylabel("광물종합지수")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()


def plot_return_rate(df, save_path: Optional[Path] = None):
    plt.figure(figsize=(18, 6))
    plt.plot(df[DATE_COL], df[RETURN_COL], label="등락율(%)", linewidth=1.3)
    if "flag_return_zscore" in df.columns:
        return_anomaly = df[df["flag_return_zscore"] == 1]
        if not return_anomaly.empty:
            plt.scatter(return_anomaly[DATE_COL], return_anomaly[RETURN_COL], s=60, label="등락율 급등락 탐지", marker="o")
    plt.axhline(df[RETURN_COL].mean(), linestyle="--", linewidth=1, label="평균 등락율")
    plt.title("등락율 기반 급등락 이상징후 탐지", fontsize=16)
    plt.xlabel("기준일")
    plt.ylabel("등락율(%)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()


def plot_volatility(df, save_path: Optional[Path] = None):
    plt.figure(figsize=(18, 6))
    plt.plot(df[DATE_COL], df[STD_COL], label="표준편차(20)", linewidth=1.5)
    if "flag_volatility" in df.columns:
        vol_anomaly = df[df["flag_volatility"] == 1]
        if not vol_anomaly.empty:
            plt.scatter(vol_anomaly[DATE_COL], vol_anomaly[STD_COL], s=60, label="변동성 확대 탐지", marker="o")
    plt.title("표준편차(20) 기반 변동성 확대 탐지", fontsize=16)
    plt.xlabel("기준일")
    plt.ylabel("표준편차(20)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()


def plot_all_results(df, save_dir: Optional[Path] = None, timestamp: Optional[str] = None):
    if save_dir is not None:
        save_dir.mkdir(parents=True, exist_ok=True)
    suffix = f"_{timestamp}" if timestamp else ""
    plot_index_with_bands(df, save_dir / f"plot_index_with_bands{suffix}.png" if save_dir is not None else None)
    plot_anomaly_grade(df, save_dir / f"plot_anomaly_grade{suffix}.png" if save_dir is not None else None)
    plot_return_rate(df, save_dir / f"plot_return_rate{suffix}.png" if save_dir is not None else None)
    plot_volatility(df, save_dir / f"plot_volatility{suffix}.png" if save_dir is not None else None)
