from graph.network_graph import NetworkGraph
from models.node import Router, Switch, Host
from models.link import NetworkLink
from routing.dijkstra import DijkstraRouter
from simulation.simulator import Simulator
from reports.report_generator import ReportGenerator


def afficher_menu():
    """Affiche le menu principal."""
    print("\n======================================")
    print("   ANALYSEUR DE TRAFIC RÉSEAU")
    print("======================================")
    print("  1. Créer un réseau")
    print("  2. Lancer la simulation")
    print("  3. Afficher le rapport")
    print("  4. Exporter rapport CSV")
    print("  5. Sauvegarder le réseau (JSON)")
    print("  6. Charger un réseau (JSON)")
    print("  0. Quitter")
    print("======================================")
    return input("Votre choix : ")


def creer_reseau():
    """Crée un réseau exemple avec quelques nœuds et liens."""
    graph = NetworkGraph()

    # Création des nœuds
    graph.ajouter_noeud(Router("R1", capacite=5))
    graph.ajouter_noeud(Router("R2", capacite=5))
    graph.ajouter_noeud(Switch("S1", capacite=10))
    graph.ajouter_noeud(Host("PC1", capacite=3))
    graph.ajouter_noeud(Host("PC2", capacite=3))

    # Création des liens
    graph.ajouter_lien(NetworkLink("PC1", "S1", bande_passante=100, latence=2))
    graph.ajouter_lien(NetworkLink("S1", "R1", bande_passante=100, latence=5))
    graph.ajouter_lien(NetworkLink("R1", "R2", bande_passante=50, latence=10))
    graph.ajouter_lien(NetworkLink("R2", "PC2", bande_passante=100, latence=2))

    print("\n✅ Réseau créé avec succès !")
    return graph


def main():
    """Point d'entrée principal du programme."""
    graph = None
    simulator = None
    reporter = None

    while True:
        choix = afficher_menu()

        if choix == "1":
            graph = creer_reseau()
            router = DijkstraRouter(graph)
            simulator = Simulator(graph, router)
            reporter = ReportGenerator(simulator)

        elif choix == "2":
            if simulator is None:
                print("\n⚠️  Créez d'abord un réseau (option 1)")
                continue
            nb_ticks = int(input("Nombre de ticks : "))
            nb_paquets = int(input("Nombre de paquets par tick : "))
            for _ in range(nb_ticks):
                for _ in range(nb_paquets):
                    simulator.generer_paquet("PC1", "PC2")
                simulator.executer_tick()
            print("\n✅ Simulation terminée !")

        elif choix == "3":
            if reporter is None:
                print("\n⚠️  Lancez d'abord une simulation (option 2)")
                continue
            print(reporter.generer_rapport_texte())

        elif choix == "4":
            if reporter is None:
                print("\n⚠️  Lancez d'abord une simulation (option 2)")
                continue
            fichier = reporter.exporter_csv()
            print(f"\n✅ Rapport exporté : {fichier}")

        elif choix == "5":
            if graph is None:
                print("\n⚠️  Créez d'abord un réseau (option 1)")
                continue
            graph.sauvegarder_json("configs/sample_network.json")
            print("\n✅ Réseau sauvegardé !")

        elif choix == "6":
            graph = NetworkGraph()
            graph.charger_json("configs/sample_network.json")
            router = DijkstraRouter(graph)
            simulator = Simulator(graph, router)
            reporter = ReportGenerator(simulator)
            print("\n✅ Réseau chargé !")

        elif choix == "0":
            print("\nAu revoir ! 👋")
            break

        else:
            print("\n⚠️  Choix invalide !")


if __name__ == "__main__":
    main()
