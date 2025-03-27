import os
import csv
from file_handler import read_file, log_results
from random_search import RandomSearch
from greedy_search import GreedySearch
from genetic_algorithm import GeneticAlgorithm
from tabu_search import TabuSearch

data_dir = "data"
results_dir = "results"
os.makedirs(results_dir, exist_ok=True)


# All algorithms are run on all instances and logs are in -> results/overall_results.csv
def run_all():
    for file_name in os.listdir(data_dir):
        if file_name.endswith(".vrp"):
            instance = read_file(os.path.join(data_dir, file_name))

            algorithms = [
                RandomSearch(**instance),
                GreedySearch(**instance),
                GeneticAlgorithm(**instance),
                TabuSearch(**instance),
            ]
            for algorithm in algorithms:
                if algorithm.__class__.__name__ == "RandomSearch":
                    number_of_runs = 10000
                elif algorithm.__class__.__name__ == "GreedySearch":
                    number_of_runs = 1
                else:
                    number_of_runs = 10

                _, best_fitness, worst_fitness, avg_fitness, std = algorithm.run(number_of_runs)
                log_results(
                    results_dir,
                    file_name,
                    algorithm.__class__.__name__,
                    best_fitness,
                    worst_fitness,
                    avg_fitness,
                    std
                )

if __name__ == "__main__":
    # Run all algorithms on all instances
    print("Running all algorithms on all instances...")
    run_all()

    print("Done! Results are in the results directory.")
