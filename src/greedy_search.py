import random
from utils import calculate_distance_matrix, calculate_fitness

class GreedySearch:
    def __init__(self, dimension, capacity, node_coords, demands, depot):
        self.dimension = dimension
        self.capacity = capacity
        self.node_coords = node_coords
        self.demands = demands
        self.depot = depot
        self.distance_matrix = calculate_distance_matrix(self.node_coords)

    def generate_greedy_solution(self):
        remaining_customers = list(range(1, self.dimension + 1))
        remaining_customers.remove(self.depot)

        routes = []
        while remaining_customers:
            current_route = [self.depot]
            current_load = 0

            while remaining_customers:
                last_customer = current_route[-1]
                nearest_customer = None
                nearest_distance = float("inf")

                for customer in remaining_customers:
                    demand = self.demands[customer - 1][1]
                    if current_load + demand <= self.capacity:
                        distance = self.distance_matrix[last_customer - 1][customer - 1]
                        if distance < nearest_distance:
                            nearest_distance = distance
                            nearest_customer = customer

                if nearest_customer is None:
                    break

                current_route.append(nearest_customer)
                current_load += self.demands[nearest_customer - 1][1]
                remaining_customers.remove(nearest_customer)

            current_route.append(self.depot)
            routes.append(current_route)

        return routes

    def generate_randomized_greedy_solution(self, random_factor=0.5, k=3):
        remaining_customers = list(range(1, self.dimension + 1))
        remaining_customers.remove(self.depot)

        routes = []
        while remaining_customers:
            current_route = [self.depot]
            current_load = 0

            while remaining_customers:
                last_customer = current_route[-1]
                nearest_customers = []

                for customer in remaining_customers:
                    demand = self.demands[customer - 1][1]
                    if current_load + demand <= self.capacity:
                        distance = self.distance_matrix[last_customer - 1][customer - 1]
                        nearest_customers.append((customer, distance))

                if not nearest_customers:
                    break

                nearest_customers.sort(key=lambda x: x[1])

                if len(nearest_customers) > k - 1 and random.random() < random_factor:
                    # Randomly select one of the top k nearest customers
                    nearest_customer = random.choice(nearest_customers[:k])[0]
                else:
                    # Select the nearest customer
                    nearest_customer = nearest_customers[0][0]

                current_route.append(nearest_customer)
                current_load += self.demands[nearest_customer - 1][1]
                remaining_customers.remove(nearest_customer)

            current_route.append(self.depot)
            routes.append(current_route)

        return routes

    def run(self, iterations=100):
        best_solution = self.generate_greedy_solution()
        best_fitness = calculate_fitness(
            best_solution, self.distance_matrix
        )
        total_fitness_sum = 0

        return (
            best_solution,
            best_fitness,
            None,
            None,
            None
        )
