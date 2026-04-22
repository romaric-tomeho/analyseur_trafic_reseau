import json
from models.node import Router, Switch, Host
from models.link import NetworkLink


class NetworkGraph:

    def __init__(self):
        self.noeuds = {}
        self.liens = {}

    def ajouter_noeud(self, noeud):
        self.noeuds[noeud.node_id] = noeud

    def supprimer_noeud(self, node_id):
        if node_id in self.noeuds:
            del self.noeuds[node_id]

    def ajouter_lien(self, lien):
        self.liens[(lien.source, lien.destination)] = lien

    def supprimer_lien(self, source, destination):
        if (source, destination) in self.liens:
            del self.liens[(source, destination)]

    def get_voisins(self, node_id):
        voisins = []
        for (source, destination), lien in self.liens.items():
            if source == node_id:
                voisins.append((destination, lien))
        return voisins

    def sauvegarder_json(self, fichier):
        data = {
            "noeuds": [
                {
                    "node_id": n.node_id,
                    "node_type": n.node_type,
                    "capacite": n.capacite
                }
                for n in self.noeuds.values()
            ],
            "liens": [
                {
                    "source": l.source,
                    "destination": l.destination,
                    "bande_passante": l.bande_passante,
                    "latence": l.latence
                }
                for l in self.liens.values()
            ]
        }
        with open(fichier, "w") as f:
            json.dump(data, f, indent=4)

    def charger_json(self, fichier):
        with open(fichier, "r") as f:
            data = json.load(f)
        for n in data["noeuds"]:
            if n["node_type"] == "router":
                noeud = Router(n["node_id"], n["capacite"])
            elif n["node_type"] == "switch":
                noeud = Switch(n["node_id"], n["capacite"])
            else:
                noeud = Host(n["node_id"], n["capacite"])
            self.ajouter_noeud(noeud)
        for l in data["liens"]:
            lien = NetworkLink(
                l["source"],
                l["destination"],
                l["bande_passante"],
                l["latence"]
            )
            self.ajouter_lien(lien)