import pandas as pd
import io
from app.core.encryption import decrypt_data

def compute_signal(encrypted_blob: bytes, signal_type: str) -> dict:
    raw_csv = decrypt_data(encrypted_blob)
    df = pd.read_csv(io.StringIO(raw_csv))
    result = {}

    if signal_type == "price_preference":
        total = len(df)
        if total == 0:
            return {}
        result = {
            "under_1000": round(len(df[df["price"] < 1000]) / total * 100, 1),
            "under_3000": round(len(df[df["price"] < 3000]) / total * 100, 1),
            "above_3000": round(len(df[df["price"] >= 3000]) / total * 100, 1),
            "avg_spend": round(float(df["price"].mean()), 2)
        }

    elif signal_type == "running_frequency":
        total = len(df)
        if total == 0:
            return {}
        result = {
            "daily": round(len(df[df["runs_per_week"] >= 6]) / total * 100, 1),
            "thrice_week": round(len(df[df["runs_per_week"].between(3, 5)]) / total * 100, 1),
            "occasional": round(len(df[df["runs_per_week"] < 3]) / total * 100, 1),
            "avg_runs": round(float(df["runs_per_week"].mean()), 1)
        }

    elif signal_type == "food_preference":
        total = len(df)
        if total == 0:
            return {}
        result = {
            "avg_order_value": round(float(df["amount"].mean()), 2),
            "orders_per_month": round(float(len(df) / 3), 1),
            "most_ordered": str(df["category"].mode()[0]) if "category" in df.columns else "unknown"
        }

    del df, raw_csv
    return result


def aggregate_signals(blobs: list, signal_type: str) -> dict:
    all_results = [compute_signal(b, signal_type) for b in blobs]
    all_results = [r for r in all_results if r]
    if not all_results:
        return {}
    keys = all_results[0].keys()
    return {
        k: round(sum(r[k] for r in all_results if isinstance(r.get(k), (int, float))) / len(all_results), 1)
        for k in keys
    }