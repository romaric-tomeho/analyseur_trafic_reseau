from abc import ABC, abstractmethod


class RoutingAlgorithm(ABC):
    def __init__(self, graph):
        self.graph = graph

    @abstractmethod
    def find_path(self, source, destination):
        pass

    @abstractmethod
    def get_next_hop(self, source, destination):
        pass