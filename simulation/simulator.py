import random
from models.packet import Packet
from models.link import NetworkLink


class Simulator:
    """Moteur central qui orchestre la simulation du trafic réseau."""

    def __init__(self, graph, router):
        self.graph = graph          # Référence au NetworkGraph
        self.router = router        # Algorithme de routage
        self.tick_actuel = 0        # Compteur de ticks
        self.paquets = []           # Liste de tous les paquets
        self.statistiques = {
            "paquets_envoyes": 0,
            "paquets_perdus": 0,
            "latence_totale": 0
        }

    def generer_paquet(self, source, destination, taille=100, priorite=1):
        """Génère un nouveau paquet et l'injecte dans le réseau."""
        packet_id = f"PKT-{self.tick_actuel}-{len(self.paquets)}"
        paquet = Packet(packet_id, source, destination, taille, priorite)
        self.paquets.append(paquet)
        self.statistiques["paquets_envoyes"] += 1
        return paquet

    def executer_tick(self):
        """Exécute un tick de simulation."""
        self.tick_actuel += 1
        for noeud in self.graph.noeuds.values():
            if noeud.etat:
                for _ in range(noeud.capacite):
                    if noeud.file_attente:
                        paquet = noeud.file_attente.popleft()
                        self._router_paquet(paquet, noeud.node_id)

    def _router_paquet(self, paquet, noeud_actuel):
        """Route un paquet vers sa destination."""
        if noeud_actuel == paquet.destination:
            return
        prochain = self.router.get_next_hop(noeud_actuel, paquet.destination)
        if prochain is None:
            self.statistiques["paquets_perdus"] += 1
            return
        lien = self.graph.liens.get((noeud_actuel, prochain))
        if lien and not lien.is_saturated():
            paquet.add_hop(prochain, lien.latence)
            self.statistiques["latence_totale"] += lien.latence
            self.graph.noeuds[prochain].file_attente.append(paquet)
        else:
            self.statistiques["paquets_perdus"] += 1

    def get_statistiques(self):
        """Retourne les statistiques de la simulation."""
        envoyes = self.statistiques["paquets_envoyes"]
        perdus = self.statistiques["paquets_perdus"]
        latence = self.statistiques["latence_totale"]
        return {
            "tick_actuel": self.tick_actuel,
            "paquets_envoyes": envoyes,
            "paquets_perdus": perdus,
            "taux_perte": round((perdus / envoyes * 100), 2) if envoyes > 0 else 0,
            "latence_moyenne": round((latence / envoyes), 2) if envoyes > 0 else 0
        }