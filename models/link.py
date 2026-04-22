class NetworkLink:
    def __init__(self, source, destination, bande_passante, latence):
        self.source = source
        self.destination = destination
        self.bande_passante = bande_passante
        self.latence = latence
        self.charge_actuelle = 0.0
        self.actif = True

    def is_saturated(self, seuil=0.8):
        if self.bande_passante == 0:
            return True
        return (self.charge_actuelle / self.bande_passante) >= seuil

    def transmit(self, paquet):
        if not self.actif:
            return False
        charge_paquet = (paquet.taille * 8) / 1_000_000
        if self.charge_actuelle + charge_paquet > self.bande_passante:
            return False
        self.charge_actuelle += charge_paquet
        paquet.latence_totale += self.latence
        return True

    def reset_charge(self):
        self.charge_actuelle = 0.0

    def get_status(self):
        return {
            "source": self.source,
            "destination": self.destination,
            "bande_passante": self.bande_passante,
            "latence": self.latence,
            "charge_actuelle": self.charge_actuelle,
            "sature": self.is_saturated()
        }