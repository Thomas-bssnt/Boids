from math import sqrt
import numpy as np


class Boid:
    boid_counter = 0

    def __init__(self, window_size):
        #
        self._dimension = len(window_size)
        self.window_size = window_size
        #
        self.speed_min = 5
        self.speed_max = 15
        #
        self.position = np.random.rand(self._dimension) * window_size
        self.velocity = self.speed_min + np.random.rand(self._dimension) * (self.speed_max - self.speed_min)
        #
        self._visual_range = 80
        self._separation_distance = 10
        self._separation_factor = 0.1
        self._alignment_factor = 0.05
        self._coherence_factor = 0.01
        #
        self.id = Boid.boid_counter
        Boid.boid_counter += 1

    @property
    def speed(self):
        # return norm(self.velocity)
        return np.linalg.norm(self.velocity)

    def _get_neighbors(self, boids, distance_matrix):
        neighbors = []
        too_close_neighbors = []
        for boid in boids:
            if boid.id != self.id:
                if distance_matrix[boid.id, self.id] < self._visual_range:
                    neighbors.append(boid)
                    if distance_matrix[boid.id, self.id] < self._separation_distance:
                        too_close_neighbors.append(boid)
        return neighbors, too_close_neighbors

    def _separation(self, too_close_neighbors):
        move = np.zeros(self._dimension)
        for boid in too_close_neighbors:
            move += (self.position - boid.position)
        return move * self._separation_factor

    def _alignment(self, neighbors):
        if neighbors:
            average_velocity = sum(boid.velocity for boid in neighbors) / len(neighbors)
            return (average_velocity - self.velocity) * self._alignment_factor
        return np.zeros(self._dimension)

    def _cohesion(self, neighbors):
        if neighbors:
            average_position = sum(boid.position for boid in neighbors) / len(neighbors)
            return (average_position - self.position) * self._coherence_factor
        return np.zeros(self._dimension)

    def _limit_speed(self):
        speed = self.speed
        if speed < self.speed_min:
            self.velocity = self.velocity / speed * self.speed_min
        elif speed > self.speed_max:
            self.velocity = self.velocity / speed * self.speed_max

    def _keep_within_bounds(self):
        boundary_perception = 100
        boundary_factor = 1

        steering = np.zeros(self._dimension)
        for dim in range(self._dimension):
            if self.position[dim] < boundary_perception:
                steering[dim] += 1
            elif self.window_size[dim] - self.position[dim] < boundary_perception:
                steering[dim] -= 1

        return steering * boundary_factor

    def update(self, boids, distance_matrix):
        neighbors, too_close_neighbors = self._get_neighbors(boids, distance_matrix)

        separation = self._separation(too_close_neighbors)
        alignment = self._alignment(neighbors)
        cohesion = self._cohesion(neighbors)

        # self.velocity += cohesion
        # self.velocity += cohesion + separation
        self.velocity += separation + alignment + cohesion

        self._limit_speed()

        self.velocity += self._keep_within_bounds()

        self.position += self.velocity


def norm(vector):
    return sqrt(sum(vi * vi for vi in vector))


def compute_distance_matrix(boids):
    number_of_boids = len(boids)
    distance_matrix = np.zeros((number_of_boids, number_of_boids))
    for i in range(number_of_boids - 1):
        for j in range(i + 1, number_of_boids):
            distance = norm(boids[i].position - boids[j].position)
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance
    return distance_matrix
