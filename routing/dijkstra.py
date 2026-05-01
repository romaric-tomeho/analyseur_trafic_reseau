import heapq
from routing.base import RoutingAlgorithm


class DijkstraRouter(RoutingAlgorithm):

    def find_path(self, source, destination):# Implémentation de l'algorithme de Dijkstra pour trouver le chemin le plus court entre la source et la destination
        distances = {node_id: float('inf') for node_id in self.graph.noeuds}
        distances[source] = 0
        predecesseurs = {node_id: None for node_id in self.graph.noeuds}
        file_priorite = [(0, source)]

        while file_priorite:
            distance_actuelle, noeud_actuel = heapq.heappop(file_priorite)

            if distance_actuelle > distances[noeud_actuel]:
                continue

            if noeud_actuel == destination:
                break

            for voisin, lien in self.graph.get_voisins(noeud_actuel):
                distance = distance_actuelle + lien.latence

                if distance < distances[voisin]:
                    distances[voisin] = distance
                    predecesseurs[voisin] = noeud_actuel
                    heapq.heappush(file_priorite, (distance, voisin))

        return self._reconstruire_chemin(predecesseurs, source, destination)

    def _reconstruire_chemin(self, predecesseurs, source, destination):# Reconstruit le chemin à partir des prédecesseurs retournés par l'algorithme de Dijkstra
        chemin = []
        noeud = destination

        while noeud is not None:
            chemin.append(noeud)
            noeud = predecesseurs[noeud]

        chemin.reverse()

        if chemin and chemin[0] == source:
            return chemin
        return []

    def get_next_hop(self, source, destination):# Retourne le prochain saut sur le chemin entre la source et la destination
        chemin = self.find_path(source, destination)

        if len(chemin) >= 2:
            return chemin[1]

        return None