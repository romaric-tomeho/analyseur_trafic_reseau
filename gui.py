import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from graph.network_graph import NetworkGraph
from models.node import Router, Switch, Host
from models.link import NetworkLink
from routing.dijkstra import DijkstraRouter
from simulation.simulator import Simulator
from reports.report_generator import ReportGenerator
from database.db_manager import DatabaseManager
from exceptions.exceptions import (
    NoeudInexistantError, ReseauVideError,
    FichierIntrouvableError, CheminInexistantError
)


class AnalyseurApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Analyseur de Trafic Réseau")
        self.root.geometry("900x650")
        self.root.configure(bg="#1e1e2e")

        self.graph = None
        self.simulator = None
        self.reporter = None
        self.db = DatabaseManager()

        self._construire_interface()

    def _construire_interface(self):
        # Titre
        titre = tk.Label(
            self.root,
            text="🌐 Analyseur de Trafic Réseau",
            font=("Courier", 18, "bold"),
            bg="#1e1e2e", fg="#cdd6f4"
        )
        titre.pack(pady=10)

        # Frame principale
        frame_main = tk.Frame(self.root, bg="#1e1e2e")
        frame_main.pack(fill="both", expand=True, padx=10, pady=5)

        # Panneau gauche — Contrôles
        frame_gauche = tk.Frame(frame_main, bg="#313244", width=280)
        frame_gauche.pack(side="left", fill="y", padx=(0, 5))
        frame_gauche.pack_propagate(False)

        tk.Label(
            frame_gauche, text="RÉSEAU",
            font=("Courier", 11, "bold"),
            bg="#313244", fg="#89b4fa"
        ).pack(pady=(10, 5))

        # Création nœud
        frame_noeud = tk.LabelFrame(
            frame_gauche, text="Ajouter un nœud",
            bg="#313244", fg="#cdd6f4",
            font=("Courier", 9)
        )
        frame_noeud.pack(fill="x", padx=8, pady=5)

        tk.Label(frame_noeud, text="ID :", bg="#313244", fg="#cdd6f4").grid(row=0, column=0, sticky="w", padx=5)
        self.entry_node_id = tk.Entry(frame_noeud, width=10, bg="#45475a", fg="#cdd6f4", insertbackground="white")
        self.entry_node_id.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_noeud, text="Type :", bg="#313244", fg="#cdd6f4").grid(row=1, column=0, sticky="w", padx=5)
        self.combo_type = ttk.Combobox(frame_noeud, values=["router", "switch", "host"], width=8, state="readonly")
        self.combo_type.set("router")
        self.combo_type.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame_noeud, text="Capacité :", bg="#313244", fg="#cdd6f4").grid(row=2, column=0, sticky="w", padx=5)
        self.entry_capacite = tk.Entry(frame_noeud, width=10, bg="#45475a", fg="#cdd6f4", insertbackground="white")
        self.entry_capacite.insert(0, "5")
        self.entry_capacite.grid(row=2, column=1, padx=5, pady=2)

        tk.Button(
            frame_noeud, text="➕ Ajouter nœud",
            command=self._ajouter_noeud,
            bg="#89b4fa", fg="#1e1e2e", font=("Courier", 9, "bold")
        ).grid(row=3, column=0, columnspan=2, pady=5)

        # Création lien
        frame_lien = tk.LabelFrame(
            frame_gauche, text="Ajouter un lien",
            bg="#313244", fg="#cdd6f4",
            font=("Courier", 9)
        )
        frame_lien.pack(fill="x", padx=8, pady=5)

        tk.Label(frame_lien, text="Source :", bg="#313244", fg="#cdd6f4").grid(row=0, column=0, sticky="w", padx=5)
        self.entry_source = tk.Entry(frame_lien, width=10, bg="#45475a", fg="#cdd6f4", insertbackground="white")
        self.entry_source.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_lien, text="Destination :", bg="#313244", fg="#cdd6f4").grid(row=1, column=0, sticky="w", padx=5)
        self.entry_destination = tk.Entry(frame_lien, width=10, bg="#45475a", fg="#cdd6f4", insertbackground="white")
        self.entry_destination.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame_lien, text="Bande pass. :", bg="#313244", fg="#cdd6f4").grid(row=2, column=0, sticky="w", padx=5)
        self.entry_bp = tk.Entry(frame_lien, width=10, bg="#45475a", fg="#cdd6f4", insertbackground="white")
        self.entry_bp.insert(0, "100")
        self.entry_bp.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(frame_lien, text="Latence (ms) :", bg="#313244", fg="#cdd6f4").grid(row=3, column=0, sticky="w", padx=5)
        self.entry_latence = tk.Entry(frame_lien, width=10, bg="#45475a", fg="#cdd6f4", insertbackground="white")
        self.entry_latence.insert(0, "5")
        self.entry_latence.grid(row=3, column=1, padx=5, pady=2)

        tk.Button(
            frame_lien, text="🔗 Ajouter lien",
            command=self._ajouter_lien,
            bg="#a6e3a1", fg="#1e1e2e", font=("Courier", 9, "bold")
        ).grid(row=4, column=0, columnspan=2, pady=5)

        # Simulation
        tk.Label(
            frame_gauche, text="SIMULATION",
            font=("Courier", 11, "bold"),
            bg="#313244", fg="#89b4fa"
        ).pack(pady=(10, 5))

        frame_sim = tk.LabelFrame(
            frame_gauche, text="Paramètres",
            bg="#313244", fg="#cdd6f4",
            font=("Courier", 9)
        )
        frame_sim.pack(fill="x", padx=8, pady=5)

        tk.Label(frame_sim, text="Source :", bg="#313244", fg="#cdd6f4").grid(row=0, column=0, sticky="w", padx=5)
        self.entry_sim_source = tk.Entry(frame_sim, width=10, bg="#45475a", fg="#cdd6f4", insertbackground="white")
        self.entry_sim_source.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_sim, text="Destination :", bg="#313244", fg="#cdd6f4").grid(row=1, column=0, sticky="w", padx=5)
        self.entry_sim_dest = tk.Entry(frame_sim, width=10, bg="#45475a", fg="#cdd6f4", insertbackground="white")
        self.entry_sim_dest.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame_sim, text="Ticks :", bg="#313244", fg="#cdd6f4").grid(row=2, column=0, sticky="w", padx=5)
        self.entry_ticks = tk.Entry(frame_sim, width=10, bg="#45475a", fg="#cdd6f4", insertbackground="white")
        self.entry_ticks.insert(0, "5")
        self.entry_ticks.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(frame_sim, text="Paquets/tick :", bg="#313244", fg="#cdd6f4").grid(row=3, column=0, sticky="w", padx=5)
        self.entry_paquets = tk.Entry(frame_sim, width=10, bg="#45475a", fg="#cdd6f4", insertbackground="white")
        self.entry_paquets.insert(0, "10")
        self.entry_paquets.grid(row=3, column=1, padx=5, pady=2)

        tk.Button(
            frame_sim, text="▶ Lancer simulation",
            command=self._lancer_simulation,
            bg="#f38ba8", fg="#1e1e2e", font=("Courier", 9, "bold")
        ).grid(row=4, column=0, columnspan=2, pady=5)

        # Boutons actions
        frame_actions = tk.Frame(frame_gauche, bg="#313244")
        frame_actions.pack(fill="x", padx=8, pady=5)

        tk.Button(
            frame_actions, text="💾 Sauvegarder JSON",
            command=self._sauvegarder_json,
            bg="#fab387", fg="#1e1e2e", font=("Courier", 9, "bold"),
            width=22
        ).pack(pady=2)

        tk.Button(
            frame_actions, text="📂 Charger JSON",
            command=self._charger_json,
            bg="#fab387", fg="#1e1e2e", font=("Courier", 9, "bold"),
            width=22
        ).pack(pady=2)

        tk.Button(
            frame_actions, text="📊 Exporter CSV",
            command=self._exporter_csv,
            bg="#94e2d5", fg="#1e1e2e", font=("Courier", 9, "bold"),
            width=22
        ).pack(pady=2)

        tk.Button(
            frame_actions, text="🕐 Historique",
            command=self._afficher_historique,
            bg="#cba6f7", fg="#1e1e2e", font=("Courier", 9, "bold"),
            width=22
        ).pack(pady=2)

        # Panneau droit — Affichage
        frame_droite = tk.Frame(frame_main, bg="#1e1e2e")
        frame_droite.pack(side="right", fill="both", expand=True)

        # Zone rapport
        tk.Label(
            frame_droite, text="RAPPORT",
            font=("Courier", 11, "bold"),
            bg="#1e1e2e", fg="#89b4fa"
        ).pack(pady=(0, 5))

        self.zone_rapport = scrolledtext.ScrolledText(
            frame_droite,
            bg="#181825", fg="#cdd6f4",
            font=("Courier", 10),
            wrap="word"
        )
        self.zone_rapport.pack(fill="both", expand=True)

        # Initialiser le graphe
        self.graph = NetworkGraph()
        self.router = None
        self._log("✅ Application démarrée. Ajoutez des nœuds et des liens pour commencer.")

    def _log(self, message):
        self.zone_rapport.insert("end", message + "\n")
        self.zone_rapport.see("end")

    def _ajouter_noeud(self):
        try:
            node_id = self.entry_node_id.get().strip()
            node_type = self.combo_type.get()
            capacite = int(self.entry_capacite.get())

            if not node_id:
                raise ValueError("L'identifiant ne peut pas être vide.")
            if capacite <= 0:
                raise ValueError("La capacité doit être positive.")

            if node_type == "router":
                noeud = Router(node_id, capacite)
            elif node_type == "switch":
                noeud = Switch(node_id, capacite)
            else:
                noeud = Host(node_id, capacite)

            self.graph.ajouter_noeud(noeud)
            self._log(f"✅ Nœud '{node_id}' ({node_type}) ajouté avec capacité {capacite}.")
            self.entry_node_id.delete(0, "end")

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def _ajouter_lien(self):
        try:
            source = self.entry_source.get().strip()
            destination = self.entry_destination.get().strip()
            bp = float(self.entry_bp.get())
            latence = float(self.entry_latence.get())

            if source not in self.graph.noeuds:
                raise NoeudInexistantError(source)
            if destination not in self.graph.noeuds:
                raise NoeudInexistantError(destination)
            if bp <= 0 or latence <= 0:
                raise ValueError("La bande passante et la latence doivent être positives.")

            lien = NetworkLink(source, destination, bp, latence)
            self.graph.ajouter_lien(lien)
            self._log(f"✅ Lien {source} → {destination} | BP: {bp} Mbps | Latence: {latence} ms")

        except NoeudInexistantError as e:
            messagebox.showerror("Erreur", str(e))
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def _lancer_simulation(self):
        try:
            if not self.graph.noeuds:
                raise ReseauVideError()

            source = self.entry_sim_source.get().strip()
            destination = self.entry_sim_dest.get().strip()
            nb_ticks = int(self.entry_ticks.get())
            nb_paquets = int(self.entry_paquets.get())

            if source not in self.graph.noeuds:
                raise NoeudInexistantError(source)
            if destination not in self.graph.noeuds:
                raise NoeudInexistantError(destination)

            self.router = DijkstraRouter(self.graph)
            chemin = self.router.trouver_chemin(source, destination)
            if not chemin:
                raise CheminInexistantError(source, destination)

            self.simulator = Simulator(self.graph, self.router)
            self.reporter = ReportGenerator(self.simulator)

            for _ in range(nb_ticks):
                self.simulator.injecter_paquets(source, destination, nb_paquets)
                self.simulator.executer_tick()

            stats = self.simulator.obtenir_statistique()
            goulots = self.simulator.obtenir_goulot()
            sim_id = self.db.sauvegarder_simulation(stats, goulots)

            self.zone_rapport.delete("1.0", "end")
            self._log(self.reporter.generer_rapport_texte())
            self._log(f"\n✅ Simulation sauvegardée en base — ID #{sim_id}")

        except (ReseauVideError, NoeudInexistantError, CheminInexistantError) as e:
            messagebox.showerror("Erreur", str(e))
        except ValueError:
            messagebox.showerror("Erreur", "Ticks et paquets doivent être des entiers positifs.")

    def _sauvegarder_json(self):
        try:
            if not self.graph.noeuds:
                raise ReseauVideError()
            self.graph.sauvegarder_json("configs/sample_network.json")
            self._log("✅ Réseau sauvegardé dans configs/sample_network.json")
        except ReseauVideError as e:
            messagebox.showerror("Erreur", str(e))

    def _charger_json(self):
        try:
            import os
            if not os.path.exists("configs/sample_network.json"):
                raise FichierIntrouvableError("configs/sample_network.json")
            self.graph = NetworkGraph()
            self.graph.charger_json("configs/sample_network.json")
            self._log("✅ Réseau chargé depuis configs/sample_network.json")
            for node_id, noeud in self.graph.noeuds.items():
                self._log(f"   - {node_id} ({noeud.node_type})")
        except FichierIntrouvableError as e:
            messagebox.showerror("Erreur", str(e))

    def _exporter_csv(self):
        try:
            if self.reporter is None:
                raise ReseauVideError()
            fichier = self.reporter.exporter_csv()
            self._log(f"✅ Rapport CSV exporté : {fichier}")
        except ReseauVideError:
            messagebox.showerror("Erreur", "Lancez d'abord une simulation.")

    def _afficher_historique(self):
        self.zone_rapport.delete("1.0", "end")
        self._log(self.db.afficher_historique())


def main():
    root = tk.Tk()
    app = AnalyseurApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
