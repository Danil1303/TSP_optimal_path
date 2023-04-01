import math
from classes import Ant
from random import random


# from classes import Point

# l1 = [Point(1, 10, 10), Point(2, 100, 100), Point(3, 80, 80), Point(4, 20, 20)]


def greedy(graph: dict[int, list[list[int], list[float]]]) -> tuple[int, list[int]]:
    order_list = [1]
    total_distance = 0
    while len(graph) != 1:
        min_distance = min(graph[order_list[-1]][1])
        min_distance_position = graph[order_list[-1]][1].index(min_distance)
        destination_point = graph[order_list[-1]][0][min_distance_position]
        del graph[order_list[-1]]
        total_distance += min_distance
        order_list.append(destination_point)
        for values in graph.values():
            if destination_point in values[0]:
                del_index = values[0].index(destination_point)
                del values[0][del_index]
                del values[1][del_index]
    return math.ceil(total_distance), order_list


def ant_algorithm(graph: dict[int, list[list[int], list[float]]], iterations: int, alpha: float, beta: float,
                  evaporation_coefficient: float, pheromone_value: float):

    Ant.delete_ants()
    for values in graph.values():
        values.append([0.1] * len(values[0]))
        Ant()
    for iteration in range(iterations):
        # Запуск каждого муравья
        for ant in Ant.ants_list:
            while len(ant.route) != len(graph):
                available_points = [point for point in graph[ant.route[-1]][0] if point not in ant.route]
                indexes = [graph[ant.route[-1]][0].index(point) for point in available_points]
                distances = [graph[ant.route[-1]][1][index] for index in indexes]
                pheromones = [graph[ant.route[-1]][2][index] for index in indexes]
                chosen_point_index = ant_calculate_probabilities(distances, pheromones, alpha, beta)
                ant.total_distance += distances[chosen_point_index]
                ant.route.append(available_points[chosen_point_index])
        # Испарение феромона на каждом пути
        for values in graph.values():
            for i in range(len(values[2])):
                values[2][i] = values[2][i] * evaporation_coefficient
        # Добавочный феромон от пробежавших муравьёв
        for i, ant in enumerate(Ant.ants_list):
            additional_pheromone = pheromone_value / ant.total_distance
            for j in range(len(ant.route) - 1):
                destination = graph[ant.route[j]][0].index(ant.route[j + 1])
                graph[ant.route[j]][2][destination] += additional_pheromone
            ant.clear_ant_info()
        yield graph


def ant_calculate_probabilities(distances: list[float], pheromones: list[int], alpha: float, beta: float) -> int:
    probabilities = []
    ant_wishes = []
    for i in range(len(distances)):
        ant_wishes.append((pheromones[i] ** alpha) * (1 / distances[i]) ** beta)
    for ant_wish in ant_wishes:
        probabilities.append(ant_wish / sum(ant_wishes))
    random_probability = random()
    probabilities_sum = 0
    for i, probability in enumerate(probabilities):
        probabilities_sum += probability
        if random_probability < probabilities_sum:
            return i


def ant_local_optimal_path(graph: dict[int, list[list[int], list[float], list[float]]]) -> tuple[int, list[int], list[float]]:
    order_list = [1]
    pheromones_list = []
    total_distance = 0
    while len(graph) != 1:
        max_pheromone = max(graph[order_list[-1]][2])
        pheromones_list.append(max_pheromone)
        index_max = graph[order_list[-1]][2].index(max_pheromone)
        total_distance += graph[order_list[-1]][1][index_max]
        destination_point = graph[order_list[-1]][0][index_max]
        del graph[order_list[-1]]
        order_list.append(destination_point)
        for values in graph.values():
            if destination_point in values[0]:
                del_index = values[0].index(destination_point)
                del values[0][del_index]
                del values[1][del_index]
                del values[2][del_index]
    return math.ceil(total_distance), order_list, pheromones_list
