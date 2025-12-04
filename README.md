# Firewall Rule Optimization with Genetic Algorithm

This project implements a multi-objective optimization approach to find optimal firewall rule orderings using a Genetic Algorithm (NSGA-II). The optimization aims to:

- Minimize the average number of rule checks per packet
- Maximize the throughput (packets per second)

## Project Structure

```
firewall-ga-optimizer/
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── data/                       # Data directory
│   ├── raw/                    # Raw log files
│   └── processed/              # Processed data files
├── notebooks/                  # Jupyter notebooks for analysis
├── results/                    # Output files
│   ├── logs/                   # Log files
│   └── plots/                  # Generated plots
├── scripts/                    # Utility scripts
│   └── run_optimization.py     # Main optimization script
└── src/                        # Source code
    └── firewall_ga/            # Core package
        ├── __init__.py
        ├── config.py           # Configuration and paths
        ├── data_preprocessing.py# Data loading and preprocessing
        ├── simulation.py       # Firewall simulation logic
        ├── ga_optimizer.py     # Genetic algorithm implementation
        └── visualization.py    # Plotting functions
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd firewall-ga-optimizer
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Optimization

1. Place your firewall log file in `data/raw/log2.csv` or specify its path using the `--input` argument.

2. Run the optimization:
   ```bash
   python scripts/run_optimization.py
   ```

3. View the results in the `results/plots/` directory.

### Command Line Arguments

- `--input`: Path to input log CSV file (default: `data/raw/log2.csv`)
- `--population`: Population size for GA (default: 50)
- `--generations`: Number of generations (default: 30)
- `--cxpb`: Crossover probability (default: 0.7)
- `--mutpb`: Mutation probability (default: 0.3)

Example with custom parameters:
```bash
python scripts/run_optimization.py --population 100 --generations 50 --cxpb 0.8 --mutpb 0.2
```

## Input Data Format

The input CSV file should contain the following columns:
- `Source Port`: Source port number
- `Destination Port`: Destination port number
- `Action`: Action taken (e.g., 'allow', 'deny', 'reset-both')
- `Elapsed Time (sec)`: Time taken for processing (for throughput calculation)

## Outputs

The script generates the following outputs:
1. **Processed Data**:
   - `data/processed/firewall_rules.csv`: Extracted firewall rules
   - `data/processed/packets_with_rule_ids.csv`: Packet data with rule IDs

2. **Results**:
   - `results/plots/pareto_front.png`: Pareto front of non-dominated solutions
   - `results/plots/fitness_evolution.png`: Evolution of fitness values
   - `results/plots/rule_hits.png`: Distribution of rule hits
   - `results/logs/ga_log.txt`: Log file with detailed execution information

## Development

For development, you can use the Jupyter notebook in the `notebooks/` directory to explore the data and experiment with different parameters.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- DEAP library for the evolutionary algorithms framework
- Pandas and NumPy for data manipulation
- Matplotlib for visualization
