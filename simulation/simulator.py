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
            "paquets_bloques": 0,
            "latence_totale": 0
        }

    def generer_paquet(self, source, destination, taille=100, priorite=1):
        packet_id = f"PKT-{self.tick_actuel}-{len(self.paquets)}"
        paquet = Packet(packet_id, source, destination, taille, priorite)
        self.paquets.append(paquet)
        self.statistiques["paquets_envoyes"] += 1
        return paquet

    def injecter_paquets(self, source, destination, nb_paquets, taille=100, priorite=1):
        for _ in range(nb_paquets):
            paquet = self.generer_paquet(source, destination, taille, priorite)
            if source in self.graph.noeuds:
                self.graph.noeuds[source].file_attente.append(paquet)

    def executer_tick(self):
        self.tick_actuel += 1

        for lien in self.graph.liens.values():
            lien.charge_precedente = lien.charge_actuelle
            lien.charge_actuelle = 0.0

        for noeud in self.graph.noeuds.values():
            if noeud.etat:
                for _ in range(noeud.capacite):
                    if noeud.file_attente:
                        paquet = noeud.file_attente.popleft()
                        self._router_paquet(paquet, noeud.node_id)

        for lien in self.graph.liens.values():
            lien.charge_precedente = lien.charge_actuelle

    def _router_paquet(self, paquet, noeud_actuel):
        if noeud_actuel == paquet.destination:
            self.statistiques["paquets_livres"] += 1
            paquet.mark_delivre()
            return

        prochain = self.router.get_next_hop(noeud_actuel, paquet.destination)

        if prochain is None:
            self.statistiques["paquets_perdus"] += 1
            paquet.mark_perdu("pas_de_chemin")
            return

        lien = self.graph.liens.get((noeud_actuel, prochain))

        if lien is None:
            self.statistiques["paquets_perdus"] += 1
            paquet.mark_perdu("lien_inexistant")
            return

        if lien.is_saturated():
            self.statistiques["paquets_perdus"] += 1
            paquet.mark_perdu("lien_sature")
            return

        charge_paquet = (paquet.taille * 8) / 1_000_000
        lien.charge_actuelle += charge_paquet
        paquet.add_hop(prochain, lien.latence)
        self.statistiques["latence_totale"] += lien.latence
        self.graph.noeuds[prochain].file_attente.append(paquet)

    def get_statistiques(self):
        envoyes = self.statistiques["paquets_envoyes"]
        perdus = self.statistiques["paquets_perdus"]
        livres = self.statistiques["paquets_livres"]
        latence = self.statistiques["latence_totale"]
        bloques = sum(len(noeud.file_attente) for noeud in self.graph.noeuds.values())
        total_non_livres = perdus + bloques
        return {
            "tick_actuel": self.tick_actuel,
            "paquets_envoyes": envoyes,
            "paquets_livres": livres,
            "paquets_perdus": perdus,
            "paquets_bloques":bloques,
            "taux_perte": round((perdus / envoyes * 100), 2) if envoyes > 0 else 0,
            "latence_moyenne": round((latence / envoyes), 2) if envoyes > 0 else 0
        }

    def get_goulots(self):
        goulots = []
        for (src, dst), lien in self.graph.liens.items():
            utilisation = lien.get_utilisation()
            if utilisation >= 80:
                goulots.append({
                    "source": src,
                    "destination": dst,
                    "utilisation": utilisation,
                    "bande_passante": lien.bande_passante
                })
        return goulots