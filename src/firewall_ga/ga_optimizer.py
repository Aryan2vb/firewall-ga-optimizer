import random
import numpy as np
from deap import base, creator, tools, algorithms
from .simulation import simulate_firewall

def setup_toolbox(rule_ids, packets_df):
    """
    Set up the DEAP toolbox for the genetic algorithm.
    
    Args:
        rule_ids: List of rule IDs to optimize
        packets_df: DataFrame containing packet data for simulation
        
    Returns:
        DEAP toolbox configured for the optimization
    """
    # Create fitness and individual types if they don't exist
    if not hasattr(creator, "FitnessMulti"):
        creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))
    if not hasattr(creator, "Individual"):
        creator.create("Individual", list, fitness=creator.FitnessMulti)

    toolbox = base.Toolbox()

    # Register individual and population creation operations
    toolbox.register(
        "individual",
        tools.initIterate,
        creator.Individual,
        lambda: random.sample(rule_ids, len(rule_ids))
    )
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evaluate(individual):
        """Evaluation function that returns a tuple of fitness values."""
        avg_checks, throughput = simulate_firewall(individual, packets_df)
        return avg_checks, throughput

    # Register genetic operators
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxPartialyMatched)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selNSGA2)

    return toolbox

def run_ga(toolbox, n_pop=50, n_gen=30, cxpb=0.7, mutpb=0.3):
    """
    Run the genetic algorithm optimization.
    
    Args:
        toolbox: Configured DEAP toolbox
        n_pop: Population size
        n_gen: Number of generations
        cxpb: Crossover probability
        mutpb: Mutation probability
        
    Returns:
        tuple: (final_population, logbook, pareto_front)
    """
    random.seed(42)
    pop = toolbox.population(n=n_pop)

    # Set up statistics
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    # Run the algorithm
    pop, log = algorithms.eaMuPlusLambda(
        pop,
        toolbox,
        mu=n_pop,
        lambda_=2 * n_pop,
        cxpb=cxpb,
        mutpb=mutpb,
        ngen=n_gen,
        stats=stats,
        verbose=True
    )

    # Extract the Pareto front
    pareto_front = tools.sortNondominated(pop, len(pop), first_front_only=True)[0]
    
    return pop, log, pareto_front
