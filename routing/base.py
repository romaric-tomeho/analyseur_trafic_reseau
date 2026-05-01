from abc import ABC, abstractmethod


class RoutingAlgorithm(ABC):# Classe de base pour les algorithmes de routage
    def __init__(self, graph):
        self.graph = graph

    @abstractmethod# Trouve un chemin entre la source et la destination, retourne une liste de nœuds représentant le chemin
    def trouver_chemin(self, source, destination):
        pass

    @abstractmethod# Retourne le prochain saut sur le chemin entre la source et la destination
    def ajout_prochain_saut(self, source, destination):
        pass