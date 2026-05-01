from collections import deque

class PacketQueue:

    def __init__(self, max_size=10, mode="fifo"):
        self.max_size = max_size
        self.mode = mode
        self.lost_packets = 0
        self.queue = deque()

    def enqueue(self, packet):# Retourne True si le paquet a été ajouté, False si la file est pleine (perte de paquet)
        if len(self.queue) >= self.max_size:
            self.lost_packets += 1
            return False

        self.queue.append(packet)
        return True

    def dequeue(self):# Retourne le paquet suivant selon le mode de la file (FIFO ou LIFO), ou None si la file est vide
        if len(self.queue) == 0:
            return None
        return self.queue.popleft()

    def snapshot(self):# Retourne une liste de dictionnaires représentant les paquets dans la file d'attente
        result = []
        for packet in self.queue:
            result.append(packet.to_dict())
        return result

    def size(self):# Retourne le nombre de paquets dans la file d'attente
        return len(self.queue)