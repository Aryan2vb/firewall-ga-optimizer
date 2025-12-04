import os
import matplotlib.pyplot as plt

def plot_pareto_front(pareto_front, save_path=None):
    """
    Plot the Pareto front from the optimization results.
    
    Args:
        pareto_front: List of individuals on the Pareto front
        save_path: Optional path to save the plot
    """
    xs = [ind.fitness.values[0] for ind in pareto_front]
    ys = [ind.fitness.values[1] for ind in pareto_front]

    plt.figure(figsize=(8, 6))
    plt.scatter(xs, ys, marker='o')
    plt.xlabel('Avg Rule Checks')
    plt.ylabel('Throughput (pkt/s)')
    plt.title('Pareto Front: Rule Checks vs Throughput')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
    
    plt.show()

def plot_fitness_evolution(logbook, save_path=None):
    """
    Plot the evolution of fitness values across generations.
    
    Args:
        logbook: DEAP logbook containing statistics
        save_path: Optional path to save the plot
    """
    gens = logbook.select("gen")
    min_vals = [v[0] for v in logbook.select("min")]
    avg_vals = [v[0] for v in logbook.select("avg")]
    max_vals = [v[0] for v in logbook.select("max")]

    plt.figure(figsize=(10, 6))
    plt.plot(gens, min_vals, 'b-', label="Best")
    plt.plot(gens, avg_vals, 'g-', label="Average")
    plt.plot(gens, max_vals, 'r-', label="Worst")
    
    plt.xlabel("Generation")
    plt.ylabel("Average Rule Checks")
    plt.title("Fitness Evolution Over Generations")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
    
    plt.show()

def plot_rule_hits(rules_df, top_n=20, save_path=None):
    """
    Plot the hit counts for the top N most frequently hit rules.
    
    Args:
        rules_df: DataFrame containing rule information with 'HitCount' column
        top_n: Number of top rules to plot
        save_path: Optional path to save the plot
    """
    # Sort rules by hit count and take top N
    top_rules = rules_df.sort_values('HitCount', ascending=False).head(top_n)
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(
        range(len(top_rules)),
        top_rules['HitCount'],
        color='skyblue',
        alpha=0.8
    )
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2.,
            height,
            f'{int(height):,}',
            ha='center',
            va='bottom',
            fontsize=8
        )
    
    plt.xticks(range(len(top_rules)), top_rules['Rule ID'], rotation=45, ha='right')
    plt.xlabel('Rule ID')
    plt.ylabel('Hit Count (log scale)')
    plt.title(f'Top {top_n} Most Frequently Hit Rules')
    plt.yscale('log')
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
    
    plt.show()
