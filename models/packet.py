import time


class Packet:

    def __init__(self, packet_id, source, destination, taille, priorite=1):
        self.packet_id = packet_id
        self.source = source
        self.destination = destination
        self.taille = taille
        self.priorite = priorite
        self.chemin = []
        self.timestamp = time.time()
        self.latence_totale = 0
        self.delivre = False
        self.raison_perte = None

    def add_hop(self, node_id, latence=0):
        self.chemin.append(node_id)
        self.latence_totale += latence

    def mark_delivre(self):
        self.delivre = True

    def mark_perdu(self, raison):
        self.raison_perte = raison

    def get_info(self):
        return {
            "packet_id": self.packet_id,
            "source": self.source,
            "destination": self.destination,
            "taille": self.taille,
            "priorite": self.priorite,
            "chemin": self.chemin,
            "latence_totale": self.latence_totale,
            "delivre": self.delivre,
            "raison_perte": self.raison_perte
        }