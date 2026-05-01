import csv
from datetime import datetime


class ReportGenerator:

    def __init__(self, simulator):
        self.simulator = simulator
        self.horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")

    def generer_rapport_texte(self):#
        stats = self.simulator.obtenir_statistique()
        goulots = self.simulator.obtenir_goulot()

        rapport = f"""
======================================
   RAPPORT DE SIMULATION RÉSEAU
   Date : {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
======================================

STATISTIQUES GÉNÉRALES
-----------------------
Ticks écoulés       : {stats['tick_actuel']}
Paquets envoyés     : {stats['paquets_envoyes']}
Paquets livrés      : {stats['paquets_livres']}
Paquets bloqués     : {stats['paquets_bloques']}
Paquets perdus      : {stats['paquets_perdus']}
Taux de perte       : {stats['taux_perte']} %
Latence moyenne     : {stats['latence_moyenne']} ms

ÉTAT DES NŒUDS
-----------------------"""

        for noeud in self.simulator.graph.noeuds.values():# Affiche l'état de chaque nœud du réseau
            rapport += f"\n  [{noeud.node_type.upper()}] {noeud.node_id}"
            rapport += f" - etat : {'Actif' if noeud.etat else 'Inactif'}"
            rapport += f" - file attente : {len(noeud.file_attente)} paquets"

        rapport += "\n\nÉTAT DES LIENS\n-----------------------"
        for (src, dst), lien in self.simulator.graph.liens.items():
            utilisation = lien.obtenir_utilisation()
            rapport += f"\n  {src} → {dst}"
            rapport += f" | Bande passante : {lien.bande_passante} Mbps"
            rapport += f" | Charge : {lien.charge_precedente:.4f} Mbps"
            rapport += f" | Utilisation : {utilisation:.2f}%"

        rapport += "\n\nGOULOTS D'ÉTRANGLEMENT\n-----------------------"
        if goulots:
            for g in goulots:
                rapport += f"\n  ⚠️  Lien {g['source']} → {g['destination']}"
                rapport += f" saturé à {g['utilisation']}%"
                rapport += f" (bande passante : {g['bande_passante']} Mbps)"
        else:
            rapport += "\n  ✅ Aucun goulot détecté"

        rapport += "\n======================================"
        return rapport

    def exporter_csv(self):# Exporte les données de simulation dans un fichier CSV
        nom_fichier = f"rapport_{self.horodatage}.csv"
        with open(nom_fichier, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "packet_id", "source", "destination",
                "taille", "priorite", "latence_totale",
                "chemin", "delivre", "raison_perte"
            ])
            for paquet in self.simulator.paquets:
                writer.writerow([
                    paquet.packet_id,
                    paquet.source,
                    paquet.destination,
                    paquet.taille,
                    paquet.priorite,
                    paquet.latence_totale,
                    " -> ".join(paquet.chemin) if paquet.chemin else "N/A",
                    paquet.delivre,
                    paquet.raison_perte
                ])
        return nom_fichier
