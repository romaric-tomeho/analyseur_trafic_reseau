from abc import ABC, abstractmethod
from collections import deque


class NetworkNode(ABC):
    def __init__(self, node_id, node_type, capacite):
        self.node_id = node_id
        self.node_type = node_type
        self.capacite = capacite
        self.etat = True
        self.file_attente = deque()

    @abstractmethod
    def process_packet(self, packet):
        pass

    @abstractmethod
    def get_status(self):
        pass


class Router(NetworkNode):
    def __init__(self, node_id, capacite):
        super().__init__(node_id, "router", capacite)
        self.table_routage = {}

    def process_packet(self, packet):
        if self.etat:
            self.file_attente.append(packet)

    def get_status(self):
        return {
            "node_id": self.node_id,
            "type": self.node_type,
            "etat": self.etat,
            "file_attente": len(self.file_attente),
            "capacite": self.capacite
        }


class Switch(NetworkNode):
    def __init__(self, node_id, capacite):
        super().__init__(node_id, "switch", capacite)
        self.table_commutation = {}

    def process_packet(self, packet):
        if self.etat:
            self.file_attente.append(packet)

    def get_status(self):
        return {
            "node_id": self.node_id,
            "type": self.node_type,
            "etat": self.etat,
            "file_attente": len(self.file_attente),
            "capacite": self.capacite
        }


class Host(NetworkNode):
    def __init__(self, node_id, capacite):
        super().__init__(node_id, "host", capacite)
        self.paquets_envoyes = []
        self.paquets_recus = []

    def process_packet(self, packet):
        if self.etat:
            self.paquets_recus.append(packet)

    def get_status(self):
        return {
            "node_id": self.node_id,
            "type": self.node_type,
            "etat": self.etat,
            "paquets_envoyes": len(self.paquets_envoyes),
            "paquets_recus": len(self.paquets_recus),
            "capacite": self.capacite
        }