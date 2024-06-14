import math


def calculate_distance_matrix(node_coords):
    num_nodes = len(node_coords)
    distance_matrix = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]

    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                x1, y1 = node_coords[i][1], node_coords[i][2]
                x2, y2 = node_coords[j][1], node_coords[j][2]
                distance_matrix[i][j] = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    return distance_matrix


# fitness = alpha * total_distance + beta * number_of_vehicles
def calculate_fitness(solution, distance_matrix, alpha=1.0, beta=100.0):
    total_distance = 0
    for route in solution:
        route_distance = 0
        for i in range(len(route) - 1):
            node1 = route[i] - 1
            node2 = route[i + 1] - 1
            route_distance += distance_matrix[node1][node2]
        total_distance += route_distance

    number_of_vehicles = len(solution)
    fitness = alpha * total_distance + beta * number_of_vehicles
    return fitness, total_distance, number_of_vehicles
