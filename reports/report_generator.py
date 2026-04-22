import csv
import json
from datetime import datetime


class ReportGenerator:
    """Transforme les données de simulation en rapports exploitables."""

    def __init__(self, simulator):
        self.simulator = simulator      # Référence au Simulator
        self.horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")

    def generer_rapport_texte(self):
        """Génère un rapport textuel de la simulation."""
        stats = self.simulator.get_statistiques()
        rapport = f"""
======================================
   RAPPORT DE SIMULATION RÉSEAU
   Date : {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
======================================

STATISTIQUES GÉNÉRALES
-----------------------
Ticks écoulés       : {stats['tick_actuel']}
Paquets envoyés     : {stats['paquets_envoyes']}
Paquets perdus      : {stats['paquets_perdus']}
Taux de perte       : {stats['taux_perte']} %
Latence moyenne     : {stats['latence_moyenne']} ms

ÉTAT DES NŒUDS
-----------------------
"""
        for noeud in self.simulator.graph.noeuds.values():
            status = noeud.get_status()
            rapport += f"  [{noeud.node_type.upper()}] {noeud.node_id} "
            rapport += f"— etat : {'Actif' if noeud.etat else 'Inactif'}\n"

        rapport += "\nGOULOTS D'ÉTRANGLEMENT\n-----------------------\n"
        for (src, dst), lien in self.simulator.graph.liens.items():
            if lien.is_saturated():
                rapport += f"  ⚠️  Lien {src} → {dst} saturé !\n"

        rapport += "======================================"
        return rapport

    def exporter_csv(self):
        """Exporte les statistiques des paquets en CSV."""
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
                    " -> ".join(paquet.chemin)
                ])
        return nom_fichier