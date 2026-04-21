from abc import ABC, abstractmethod
from collections import deque

class NetworkNode(ABC) :
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