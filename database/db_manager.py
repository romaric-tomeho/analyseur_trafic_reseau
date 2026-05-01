import sqlite3
from datetime import datetime


class DatabaseManager:

    def __init__(self, db_path="database/simulation.db"):
        self.db_path = db_path
        self._initialiser_base()

    def _get_connexion(self):# Retourne une connexion à la base de données SQLite
        return sqlite3.connect(self.db_path)

    def _initialiser_base(self):# Crée les tables nécessaires dans la base de données si elles n'existent pas déjà
        with self._get_connexion() as conn:
            curseur = conn.cursor()
            curseur.execute("""
                CREATE TABLE IF NOT EXISTS simulations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    ticks INTEGER NOT NULL,
                    paquets_envoyes INTEGER NOT NULL,
                    paquets_livres INTEGER NOT NULL,
                    paquets_perdus INTEGER NOT NULL,
                    taux_perte REAL NOT NULL,
                    latence_moyenne REAL NOT NULL
                )
            """)
            curseur.execute("""
                CREATE TABLE IF NOT EXISTS goulots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    simulation_id INTEGER NOT NULL,
                    source TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    utilisation REAL NOT NULL,
                    bande_passante REAL NOT NULL,
                    FOREIGN KEY (simulation_id) REFERENCES simulations(id)
                )
            """)
            conn.commit()

    def sauvegarder_simulation(self, stats, goulots):# Sauvegarde les statistiques de la simulation et les goulots d'étranglement dans la base de données, retourne l'ID de la simulation sauvegardée
        with self._get_connexion() as conn:
            curseur = conn.cursor()
            curseur.execute("""
                INSERT INTO simulations
                (date, ticks, paquets_envoyes, paquets_livres,
                 paquets_perdus, taux_perte, latence_moyenne)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                stats["tick_actuel"],
                stats["paquets_envoyes"],
                stats["paquets_livres"],
                stats["paquets_perdus"],
                stats["taux_perte"],
                stats["latence_moyenne"]
            ))
            simulation_id = curseur.lastrowid

            for g in goulots:
                curseur.execute("""
                    INSERT INTO goulots
                    (simulation_id, source, destination, utilisation, bande_passante)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    simulation_id,
                    g["source"],
                    g["destination"],
                    g["utilisation"],
                    g["bande_passante"]
                ))
            conn.commit()
            return simulation_id

    def get_historique(self):# Récupère l'historique des simulations sauvegardées dans la base de données, retourne une liste de tuples avec les détails de chaque simulation
        with self._get_connexion() as conn:
            curseur = conn.cursor()
            curseur.execute("""
                SELECT id, date, ticks, paquets_envoyes,
                       paquets_perdus, taux_perte, latence_moyenne
                FROM simulations
                ORDER BY id DESC
            """)
            return curseur.fetchall()

    def get_simulation(self, simulation_id):# Récupère les détails d'une simulation spécifique et ses goulots d'étranglement à partir de la base de données, retourne un tuple avec les données de la simulation et une liste de goulots
        with self._get_connexion() as conn:
            curseur = conn.cursor()
            curseur.execute("""
                SELECT * FROM simulations WHERE id = ?
            """, (simulation_id,))
            simulation = curseur.fetchone()

            curseur.execute("""
                SELECT source, destination, utilisation, bande_passante
                FROM goulots WHERE simulation_id = ?
            """, (simulation_id,))
            goulots = curseur.fetchall()

            return simulation, goulots

    def afficher_historique(self):# Affiche l'historique des simulations sauvegardées dans la base de données sous forme de texte formaté
        historique = self.get_historique()
        if not historique:
            return "\n  Aucune simulation sauvegardée."

        texte = "\n======================================\n"
        texte += "   HISTORIQUE DES SIMULATIONS\n"
        texte += "======================================\n"
        for ligne in historique:
            texte += f"\n  ID #{ligne[0]} — {ligne[1]}"
            texte += f"\n    Ticks         : {ligne[2]}"
            texte += f"\n    Paquets       : {ligne[3]} envoyés, {ligne[4]} perdus"
            texte += f"\n    Taux de perte : {ligne[5]} %"
            texte += f"\n    Latence moy.  : {ligne[6]} ms"
            texte += "\n  " + "-" * 36
        texte += "\n======================================"
        return texte
