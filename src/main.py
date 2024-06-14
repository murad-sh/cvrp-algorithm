import os
import csv
from file_handler import read_file, log_results
from random_search import RandomSearch
from greedy_search import GreedySearch
from genetic_algorithm import GeneticAlgorithm

data_dir = "data"
results_dir = "results"
os.makedirs(results_dir, exist_ok=True)


# All algorithms are run on all instances and logs are in -> results/overall_results.csv
def run_all():
    for file_name in os.listdir(data_dir):
        if file_name.endswith(".vrp"):
            instance = read_file(os.path.join(data_dir, file_name))

            # Random Search
            random_search = RandomSearch(**instance)
            best_solution, best_fitness, worst_fitness, avg_fitness, _, _ = (
                random_search.run(1000)
            )
            log_results(
                results_dir,
                file_name,
                "Random Search",
                best_fitness,
                worst_fitness,
                avg_fitness,
            )

            # Greedy Search
            greedy_search = GreedySearch(**instance)
            best_solution, best_fitness, worst_fitness, avg_fitness, _, _ = (
                greedy_search.run(1000)
            )
            log_results(
                results_dir,
                file_name,
                "Greedy Search",
                best_fitness,
                worst_fitness,
                avg_fitness,
            )

            # Genetic Algorithm
            ga = GeneticAlgorithm(**instance)
            best_solution, best_fitness, worst_fitness, avg_fitness, _, _ = ga.run(
                generations=1000
            )
            log_results(
                results_dir,
                file_name,
                "Genetic Algorithm",
                best_fitness,
                worst_fitness,
                avg_fitness,
            )


# Run experiments on population size, crossover rate, and mutation rate for GA -> results/population_experiment.csv, results/crossover_experiment.csv, results/mutation_experiment.csv
def run_experiment(instance, filename, variable, values):
    with open(os.path.join(results_dir, filename), "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Parameter Value", "Best", "Worst", "Avg"])

        for value in values:
            algorithm = GeneticAlgorithm(**instance)

            if variable == "population_size":
                best_solution, best_fitness, worst_fitness, avg_fitness, _, _ = (
                    algorithm.run(population_size=value)
                )
            elif variable == "crossover_rate":
                best_solution, best_fitness, worst_fitness, avg_fitness, _, _ = (
                    algorithm.run(crossover_rate=value)
                )
            elif variable == "mutation_rate":
                best_solution, best_fitness, worst_fitness, avg_fitness, _, _ = (
                    algorithm.run(mutation_rate=value)
                )

            writer.writerow([value, best_fitness, worst_fitness, avg_fitness])


if __name__ == "__main__":
    # Run all algorithms on all instances
    print("Running all algorithms on all instances...")
    run_all()
    print("Done!")

    # Experiment on population size, crossover rate, and mutation rate
    instance = read_file("data/A-n80-k10.vrp")
    population_sizes = [50, 100, 200, 400, 500]
    crossover_rates = [0.3, 0.4, 0.5, 0.7, 0.9]
    mutation_rates = [0.01, 0.1, 0.2, 0.3, 0.5]

    print(
        "Running experiments on population size, crossover rate, and mutation rate..."
    )

    print("Population size experiment...")
    run_experiment(
        instance, "population_experiment.csv", "population_size", population_sizes
    )

    print("Crossover rate experiment...")
    run_experiment(
        instance, "crossover_experiment.csv", "crossover_rate", crossover_rates
    )

    print("Mutation rate experiment...")
    run_experiment(instance, "mutation_experiment.csv", "mutation_rate", mutation_rates)

    print("Done! Results are in the results directory.")
