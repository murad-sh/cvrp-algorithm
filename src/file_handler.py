import csv
import os


def read_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    node_coords_section = False
    demand_section = False
    depot_section = False
    dimension = 0
    capacity = 0
    node_coords = []
    demands = []
    depot = None

    for line in lines:
        line = line.strip()
        if line.startswith("DIMENSION"):
            dimension = int(line.split()[-1])
        elif line.startswith("CAPACITY"):
            capacity = int(line.split()[-1])
        elif line.startswith("NODE_COORD_SECTION"):
            node_coords_section = True
        elif line.startswith("DEMAND_SECTION"):
            node_coords_section = False
            demand_section = True
        elif line.startswith("DEPOT_SECTION"):
            demand_section = False
            depot_section = True
        elif node_coords_section:
            parts = line.split()
            node_coords.append((int(parts[0]), int(parts[1]), int(parts[2])))
        elif demand_section:
            parts = line.split()
            demands.append((int(parts[0]), int(parts[1])))
        elif depot_section:
            parts = line.split()
            if int(parts[0]) == -1:
                depot_section = False
            else:
                depot = int(parts[0])

    return {
        "dimension": dimension,
        "capacity": capacity,
        "node_coords": node_coords,
        "demands": demands,
        "depot": depot,
    }


def log_results(results_dir, file_name, algo_name, best, worst=None, avg=None):
    full_file_path = os.path.join(results_dir, "overall_results.csv")
    os.makedirs(results_dir, exist_ok=True)
    file_exists = os.path.isfile(full_file_path)

    with open(full_file_path, "a", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        if not file_exists:
            writer.writerow(
                [
                    "File Name",
                    "Algorithm",
                    "Best Fitness",
                    "Worst Fitness",
                    "Average Fitness",
                ]
            )
        writer.writerow([file_name, algo_name, best, worst, avg])
