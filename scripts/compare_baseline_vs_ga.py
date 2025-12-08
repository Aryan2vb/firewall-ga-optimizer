# scripts/compare_baseline_vs_ga.py


import sys
import os

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)


import matplotlib.pyplot as plt
from src.firewall_ga.data_preprocessing import build_rules_and_packets, load_raw_logs
from src.firewall_ga.simulation import simulate_firewall
from src.firewall_ga.ga_optimizer import run_ga, setup_toolbox

def compare_baseline_vs_ga(log_path="data/raw/log2.csv", ngen=30, pop_size=50, out_dir="results/plots"):
    # ensure output dir
    os.makedirs(out_dir, exist_ok=True)

    # 1. Load and preprocess
    df_raw = load_raw_logs(log_path)
    rules_df, packets_df = build_rules_and_packets(df_raw)
    print("\n===== DEBUG: RULES_DF COLUMNS =====")
    print(rules_df.columns)
    print(rules_df.head())
    print("===================================\n")


    rule_ids = list(rules_df["Rule ID"])
    baseline_order = rule_ids[:]  # original order

    # 2. Run GA to get optimized order
    toolbox = setup_toolbox(rule_ids, packets_df)
    pop, logbook, pareto_front = run_ga(toolbox, n_gen=ngen, n_pop=pop_size)

    if not pareto_front:
        raise RuntimeError("Pareto front is empty — GA failed or returned no individuals.")

    # pick best individual (safe: check type)
    best_ind = pareto_front[0]
    ga_order = list(best_ind)

    # 3. Simulate baseline and GA, collecting per-packet time
    baseline_metrics = simulate_firewall(baseline_order, packets_df, return_times=True)
    ga_metrics = simulate_firewall(ga_order, packets_df, return_times=True)

    # Expect dictionaries with 'packet_times' key
    baseline_times = baseline_metrics.get("packet_times")
    ga_times = ga_metrics.get("packet_times")

    if baseline_times is None or ga_times is None:
        raise RuntimeError("simulate_firewall did not return packet_times. Make sure return_times=True is supported.")

    # 4. Plot average time per packet (bar)
    avg_baseline = sum(baseline_times) / len(baseline_times)
    avg_ga = sum(ga_times) / len(ga_times)

    plt.figure(figsize=(6,4))
    plt.bar(["Baseline", "GA-optimized"], [avg_baseline, avg_ga])
    plt.ylabel("Average time per packet (sec)")
    plt.title("Baseline vs GA-optimized average processing time")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "baseline_vs_ga_avg_time.png"))
    plt.close()

    # 5. Plot distribution (boxplot)
    plt.figure(figsize=(6,4))
    plt.boxplot([baseline_times, ga_times], labels=["Baseline", "GA-optimized"])
    plt.ylabel("Time per packet (sec)")
    plt.title("Distribution of per-packet processing time")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "baseline_vs_ga_time_boxplot.png"))
    plt.close()

    print(f"Saved plots to {out_dir}")

if __name__ == "__main__":
    compare_baseline_vs_ga()
