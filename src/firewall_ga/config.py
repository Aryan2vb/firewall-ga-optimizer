import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")

LOG_FILE = os.path.join(RESULTS_DIR, "logs", "ga_log.txt")

LOG_CSV_PATH = os.path.join(RAW_DATA_DIR, "log2.csv")
FIREWALL_RULES_PATH = os.path.join(PROCESSED_DATA_DIR, "firewall_rules.csv")
PACKETS_WITH_RULE_IDS_PATH = os.path.join(PROCESSED_DATA_DIR, "packets_with_rule_ids.csv")
