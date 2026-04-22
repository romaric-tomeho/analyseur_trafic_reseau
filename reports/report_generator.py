import csv
from datetime import datetime


class ReportGenerator:

    def __init__(self, simulator):
        self.simulator = simulator
        self.horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")

    def generer_rapport_texte(self):
        stats = self.simulator.get_statistiques()

        rapport = f"""
   RAPPORT DE SIMULATION RÉSEAU
   Date : {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

STATISTIQUES GÉNÉRALES
-----------------------
Ticks écoulés       : {stats['tick_actuel']}
Paquets envoyés     : {stats['paquets_envoyes']}
Paquets livrés      : {stats['paquets_livres']}
Paquets perdus      : {stats['paquets_perdus']}
Taux de perte       : {stats['taux_perte']} %
Latence moyenne     : {stats['latence_moyenne']} ms

ÉTAT DES NŒUDS
-----------------------
"""

        for noeud in self.simulator.graph.noeuds.values():
            rapport += f"  [{noeud.node_type.upper()}] {noeud.node_id} "
            rapport += f"- etat : {'Actif' if noeud.etat else 'Inactif'}\n"

        rapport += "\nGOULOTS D'ÉTRANGLEMENT\n-----------------------\n"

        for (src, dst), lien in self.simulator.graph.liens.items():
            if lien.is_saturated():
                rapport += f"  ⚠️  Lien {src} -> {dst} saturé !\n"

        return rapport

    def exporter_csv(self):
        nom_fichier = f"rapport_{self.horodatage}.csv"

        with open(nom_fichier, "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow([
                "packet_id", "source", "destination",
                "taille", "priorite", "latence_totale", "chemin"
            ])

            for paquet in self.simulator.paquets:
                writer.writerow([
                    paquet.packet_id,
                    paquet.source,
                    paquet.destination,
                    paquet.taille,
                    paquet.priorite,
                    paquet.latence_totale,
                    " -> ".join(paquet.chemin) if paquet.chemin else "N/A"
                ])

        return nom_fichier  