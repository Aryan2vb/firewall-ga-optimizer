import numpy as np
import pandas as pd
from typing import List, Dict, Any

def simulate_firewall(rule_order: List[Any], packets_df: pd.DataFrame, return_times: bool = False) -> Dict[str, Any]:
    """
    Simulate firewall performance using reordered rules.

    Args:
        rule_order: List of rule IDs in new order
        packets_df: DataFrame with columns ['Rule ID', 'HitCount', 'Elapsed Time (sec)']
        return_times: If True, also return per-packet simulated times list

    Returns:
        dict with:
            - avg_checks: average (match_index * hitcount)
            - throughput: packets per second
            - packet_times: list of per-packet times (only if return_times=True)
    """

    # Map rule → its position in reordered list
    rule_index_map = {rule_id: idx for idx, rule_id in enumerate(rule_order)}

    packets = packets_df.copy()

    # Match Index = position of rule hit
    packets["Match Index"] = packets["Rule ID"].map(rule_index_map)

    # HitCount fallback
    packets["HitCount"] = packets["HitCount"].fillna(1)

    # Weighted checks (your original logic)
    packets["Weighted Checks"] = packets["Match Index"] * packets["HitCount"]

    # Average number of rule checks
    avg_checks = packets["Weighted Checks"].mean()

    # Throughput calculation from original CSV time
    elapsed = packets["Elapsed Time (sec)"].replace(0, np.nan).dropna()
    throughput = len(packets) / elapsed.mean()

    # -----------------------------
    # OPTIONAL: Per-packet times (for visualization)
    # -----------------------------
    packet_times = None
    if return_times:
        # Using Weighted Checks as simulated cost → more realistic than perf_counter
        packet_times = packets["Weighted Checks"].tolist()

    # Build output
    result = {
        "avg_checks": avg_checks,
        "throughput": throughput,
    }

    if return_times:
        result["packet_times"] = packet_times

    return result


def run_baseline_and_ga():
    # 1) run baseline rule order simulation
    # 2) run GA + best individual
    # 3) build and return metrics as dict
    return {
        "baseline": {
            "avg_checks": 10.5,
            "avg_time": 0.00042,
            "throughput": 12000,
            "per_rules": [
                {"rule_id": "R1", "position": 1, "hit_count": 5000, "total_time": 0.2},
                # ...
            ]
        },
        "ga_best": {
            "avg_checks": 6.1,
            "avg_time": 0.00029,
            "throughput": 17000,
            "per_rules": [
                {"rule_id": "R5", "position": 1, "hit_count": 8000, "total_time": 0.18},
                # ...
            ]
        },
        "pareto": [
            {"avg_checks": 8.3, "avg_time": 0.00035, "is_baseline": True, "is_selected": False},
            {"avg_checks": 6.1, "avg_time": 0.00029, "is_baseline": False, "is_selected": True},
            # ...
        ]
    }
