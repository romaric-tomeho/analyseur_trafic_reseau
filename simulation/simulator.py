import random
from models.packet import Packet


class Simulator:

    def __init__(self, graph, router):
        self.graph = graph
        self.router = router
        self.tick_actuel = 0
        self.paquets = []
        self.statistiques = {
            "paquets_envoyes": 0,
            "paquets_perdus": 0,
            "paquets_livres": 0,
            "latence_totale": 0
        }

    def generer_paquet(self, source, destination, taille=100, priorite=1):
        """Génère un nouveau paquet et l'injecte dans le réseau."""
        packet_id = f"PKT-{self.tick_actuel}-{len(self.paquets)}"
        paquet = Packet(packet_id, source, destination, taille, priorite)

        self.paquets.append(paquet)
        self.statistiques["paquets_envoyes"] += 1

        # Injection dans la file du noeud source
        self.graph.noeuds[source].file_attente.append(paquet)

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

        # Si le paquet est arrivé
        if noeud_actuel == paquet.destination:
            self.statistiques["paquets_livres"] += 1
            return

        prochain = self.router.get_next_hop(noeud_actuel, paquet.destination)

        if prochain is None:
            self.statistiques["paquets_perdus"] += 1
            return

        lien = self.graph.liens.get((noeud_actuel, prochain))

        if lien and not lien.is_saturated():
            paquet.add_hop(prochain, lien.latence)
            self.statistiques["latence_totale"] += lien.latence

            # Envoi vers le noeud suivant
            self.graph.noeuds[prochain].file_attente.append(paquet)
        else:
            self.statistiques["paquets_perdus"] += 1

    def get_statistiques(self):
        """Retourne les statistiques de la simulation."""
        envoyes = self.statistiques["paquets_envoyes"]
        perdus = self.statistiques["paquets_perdus"]
        livres = self.statistiques["paquets_livres"]
        latence = self.statistiques["latence_totale"]

        paquets_reussis = livres if livres > 0 else 1  # éviter division par 0

        return {
            "tick_actuel": self.tick_actuel,
            "paquets_envoyes": envoyes,
            "paquets_perdus": perdus,
            "paquets_livres": livres,
            "taux_perte": round((perdus / envoyes * 100), 2) if envoyes > 0 else 0,
            "latence_moyenne": round((latence / paquets_reussis), 2)
        }