class NoeudInexistantError(Exception):
    """Levée quand un nœud demandé n'existe pas dans le graphe."""
    def __init__(self, node_id):
        super().__init__(f"Le nœud '{node_id}' n'existe pas dans le réseau.")
        self.node_id = node_id


class LienInexistantError(Exception):
    """Levée quand un lien demandé n'existe pas."""
    def __init__(self, source, destination):
        super().__init__(f"Aucun lien entre '{source}' et '{destination}'.")
        self.source = source
        self.destination = destination


class ReseauVideError(Exception):
    """Levée quand on tente une simulation sur un réseau vide."""
    def __init__(self):
        super().__init__("Le réseau est vide. Ajoutez des nœuds avant de simuler.")


class FichierIntrouvableError(Exception):
    """Levée quand un fichier JSON ou CSV est introuvable."""
    def __init__(self, fichier):
        super().__init__(f"Fichier introuvable : '{fichier}'.")
        self.fichier = fichier


class CapaciteInvalideError(Exception):
    """Levée quand la capacité ou la bande passante est invalide."""
    def __init__(self, valeur):
        super().__init__(f"Valeur invalide : '{valeur}'. Doit être un nombre positif.")
        self.valeur = valeur


class CheminInexistantError(Exception):
    """Levée quand aucun chemin n'existe entre source et destination."""
    def __init__(self, source, destination):
        super().__init__(f"Aucun chemin trouvé entre '{source}' et '{destination}'.")
        self.source = source
        self.destination = destination
