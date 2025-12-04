import pandas as pd
import numpy as np
from .config import (
    LOG_CSV_PATH,
    FIREWALL_RULES_PATH,
    PACKETS_WITH_RULE_IDS_PATH,
    PROCESSED_DATA_DIR,
)
import os

RULE_COLS = ['Source Port', 'Destination Port', 'Action']

def load_raw_logs(path: str = LOG_CSV_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df['Action'] = (
        df['Action']
        .str.lower()
        .map({
            'allow': 'allow',
            'deny': 'deny',
            'reset-both': 'deny'
        })
        .fillna('deny')
    )
    return df

def build_rules_and_packets(df: pd.DataFrame):
    # Extract rules
    rules_df = df[RULE_COLS].drop_duplicates().reset_index(drop=True)
    rules_df['Rule ID'] = rules_df.index

    # Count frequency
    hit_counts = df.groupby(RULE_COLS).size().reset_index(name='HitCount')
    rules_df = rules_df.merge(hit_counts, on=RULE_COLS, how='left')

    # Merge packets
    full_df = df.merge(rules_df, on=RULE_COLS, how='left')

    # Save processed data
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    rules_df.to_csv(FIREWALL_RULES_PATH, index=False)
    full_df.to_csv(PACKETS_WITH_RULE_IDS_PATH, index=False)

    return rules_df, full_df
