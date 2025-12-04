import numpy as np
import pandas as pd

def simulate_firewall(rule_order, packets_df: pd.DataFrame):
    """
    Simulate firewall operation with given rule order.
    
    Args:
        rule_order: List of rule IDs in the order they should be checked
        packets_df: DataFrame containing packet data with 'Rule ID', 'HitCount', and 'Elapsed Time (sec)' columns
        
    Returns:
        tuple: (average_checks, throughput) - Average number of rules checked per packet and packets per second
    """
    rule_index_map = {rule_id: idx for idx, rule_id in enumerate(rule_order)}

    packets = packets_df.copy()
    packets['Match Index'] = packets['Rule ID'].map(rule_index_map)

    packets['HitCount'] = packets['HitCount'].fillna(1)
    packets['Weighted Checks'] = packets['Match Index'] * packets['HitCount']

    avg_checks = packets['Weighted Checks'].mean()

    elapsed = packets['Elapsed Time (sec)'].replace(0, np.nan).dropna()
    throughput = len(packets) / elapsed.mean()

    return avg_checks, throughput
