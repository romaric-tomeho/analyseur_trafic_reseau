class NetworkLink:

    def __init__(self, source, destination, bande_passante, latence):
        self.source = source
        self.destination = destination
        self.bande_passante = bande_passante
        self.latence = latence
        self.charge_actuelle = 0.0
        self.charge_precedente = 0.0
        self.actif = True
        
    def is_saturated(self, seuil=0.8):# Seuil de saturation par défaut à 80%
        if self.bande_passante == 0:
            return True
        return (self.charge_actuelle / self.bande_passante) >= seuil

    def transmit(self, paquet):# Retourne True si la transmission est réussie, False si le lien est saturé ou inactif
        if not self.actif:
            return False
        charge_paquet = (paquet.taille * 8) / 1_000_000
        if self.charge_actuelle + charge_paquet > self.bande_passante:
            return False
        self.charge_actuelle += charge_paquet
        paquet.latence_totale += self.latence
        return True

    def obtenir_utilisation(self):# Retourne l'utilisation du lien en pourcentage
        if self.bande_passante == 0:
            return 100.0
        return round((self.charge_precedente / self.bande_passante) * 100, 2)

    def status(self):# Retourne le statut du lien
        return {
            "source": self.source,
            "destination": self.destination,
            "bande_passante": self.bande_passante,
            "latence": self.latence,
            "charge_actuelle": self.charge_precedente,
            "utilisation": self.obtenir_utilisation(),
            "sature": self.is_saturated()
        }