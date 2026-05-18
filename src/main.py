from .data_loader import load_raw_data
from .preprocessing import prepare_dataframe
from .anomaly_rules import apply_anomaly_detection, build_anomaly_list
from .save_results import save_results
from .visualization import plot_all_results
from .config import RESULT_DIR


def main() -> None:
    df = load_raw_data()
    df_model = prepare_dataframe(df)
    df_model = apply_anomaly_detection(df_model)
    anomaly_list = build_anomaly_list(df_model)
    paths = save_results(df_model, anomaly_list)

    print("=== KOMIR_proj Anomaly Detection 결과 ===")
    print(f"- raw rows: {len(df):,}")
    print(f"- model rows: {len(df_model):,}")
    print(f"- saved full result: {paths['full']}")
    print(f"- saved anomaly list: {paths['list']}")

    plot_all_results(df_model, save_dir=RESULT_DIR, timestamp=paths["timestamp"])
    print(f"- saved plot files in: {RESULT_DIR}")


if __name__ == "__main__":
    main()
