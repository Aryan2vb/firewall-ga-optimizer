#!/usr/bin/env python3
"""
Firewall Rule Optimization using Genetic Algorithm

This script implements a multi-objective optimization approach to find optimal
firewall rule orderings that minimize average rule checks and maximize throughput.
"""

import os
import logging
import argparse
from pathlib import Path
import pandas as pd

# Add project root to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.firewall_ga.config import (
    FIREWALL_RULES_PATH,
    PACKETS_WITH_RULE_IDS_PATH,
    PLOTS_DIR,
    LOG_FILE
)
from src.firewall_ga.data_preprocessing import load_raw_logs, build_rules_and_packets
from src.firewall_ga.ga_optimizer import setup_toolbox, run_ga
from src.firewall_ga.simulation import simulate_firewall
from src.firewall_ga.visualization import (
    plot_pareto_front,
    plot_fitness_evolution,
    plot_rule_hits
)

def setup_logging(log_file):
    """Configure logging to both console and file."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Firewall Rule Optimization with GA')
    parser.add_argument('--input', type=str, default=None,
                      help='Path to input log CSV file')
    parser.add_argument('--population', type=int, default=50,
                      help='Population size for GA (default: 50)')
    parser.add_argument('--generations', type=int, default=30,
                      help='Number of generations (default: 30)')
    parser.add_argument('--cxpb', type=float, default=0.7,
                      help='Crossover probability (default: 0.7)')
    parser.add_argument('--mutpb', type=float, default=0.3,
                      help='Mutation probability (default: 0.3)')
    return parser.parse_args()

def main():
    """Main function to run the firewall rule optimization."""
    args = parse_args()
    logger = setup_logging(LOG_FILE)
    
    logger.info("Starting Firewall Rule Optimization")
    logger.info(f"Parameters: Population={args.population}, Generations={args.generations}, "
               f"Crossover Prob={args.cxpb}, Mutation Prob={args.mutpb}")
    
    try:
        # Load and preprocess data
        logger.info("Loading and preprocessing data...")
        raw_df = load_raw_logs(args.input) if args.input else load_raw_logs()
        rules_df, full_df = build_rules_and_packets(raw_df)
        
        # Basic statistics
        logger.info(f"Loaded {len(raw_df):,} packet records")
        logger.info(f"Extracted {len(rules_df):,} unique rules")
        
        # Plot rule hit distribution
        plot_rule_hits(
            rules_df, 
            top_n=min(20, len(rules_df)),
            save_path=os.path.join(PLOTS_DIR, "rule_hits.png")
        )
        
        # Setup and run GA
        logger.info("Setting up genetic algorithm...")
        rule_ids = list(rules_df['Rule ID'])
        toolbox = setup_toolbox(rule_ids, full_df)
        
        logger.info("Running genetic algorithm...")
        pop, log, pareto_front = run_ga(
            toolbox,
            n_pop=args.population,
            n_gen=args.generations,
            cxpb=args.cxpb,
            mutpb=args.mutpb
        )
        
        # Evaluate baseline (original) rule order
        baseline_order = rule_ids
        baseline_checks, baseline_throughput = simulate_firewall(baseline_order, full_df)
        
        # Get best solution (prioritizing throughput)
        best_solution = max(pop, key=lambda ind: ind.fitness.values[1])
        opt_checks, opt_throughput = simulate_firewall(best_solution, full_df)
        
        # Print results
        print("\n=== Optimization Results ===")
        print(f"Baseline - Avg Checks: {baseline_checks:.2f}, Throughput: {baseline_throughput:.2f} pkt/s")
        print(f"Optimized - Avg Checks: {opt_checks:.2f}, Throughput: {opt_throughput:.2f} pkt/s")
        print(f"Improvement: {((baseline_checks/opt_checks - 1) * 100):.1f}% fewer checks, {((opt_throughput/baseline_throughput - 1) * 100):.1f}% higher throughput")
        
        # Generate plots
        logger.info("Generating visualizations...")
        plot_pareto_front(
            pareto_front,
            save_path=os.path.join(PLOTS_DIR, "pareto_front.png")
        )
        
        plot_fitness_evolution(
            log,
            save_path=os.path.join(PLOTS_DIR, "fitness_evolution.png")
        )
        
        logger.info("Optimization completed successfully!")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
