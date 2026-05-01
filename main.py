from graph.network_graph import NetworkGraph
from models.node import Router, Switch, Host
from models.link import NetworkLink
from routing.dijkstra import DijkstraRouter
from simulation.simulator import Simulator
from reports.report_generator import ReportGenerator
from database.db_manager import DatabaseManager
from exceptions.exceptions import (
    NoeudInexistantError, ReseauVideError,
    FichierIntrouvableError, CapaciteInvalideError,
    CheminInexistantError
)


def afficher_menu():
    print("\n======================================")
    print("     ANALYSEUR DE TRAFIC RÉSEAU")
    print("======================================")
    print("  1. Créer un réseau")
    print("  2. Lancer la simulation")
    print("  3. Afficher le rapport")
    print("  4. Exporter rapport CSV")
    print("  5. Sauvegarder le réseau (JSON)")
    print("  6. Charger un réseau (JSON)")
    print("  7. Historique des simulations")
    print("  0. Quitter")
    print("======================================")
    return input("Votre choix : ")


def saisir_nombre(message, type_val=float):
    while True:
        try:
            valeur = type_val(input(message))
            if valeur <= 0:
                raise CapaciteInvalideError(valeur)
            return valeur
        except ValueError:
            print("  ⚠️  Veuillez entrer un nombre valide.")
        except CapaciteInvalideError as e:
            print(f"  ⚠️  {e}")


def creer_reseau():
    graph = NetworkGraph()

    try:
        nb_noeuds = int(saisir_nombre("Combien de nœuds voulez-vous créer ? ", int))

        for i in range(nb_noeuds):
            print(f"\nNœud {i + 1} :")
            node_id = input("  Identifiant (ex: R1, PC1, S1) : ").strip()
            node_type = input("  Type (router/switch/host) : ").strip().lower()
            capacite = int(saisir_nombre("  Capacité (paquets/tick) : ", int))

            if node_type == "router":
                noeud = Router(node_id, capacite)
            elif node_type == "switch":
                noeud = Switch(node_id, capacite)
            elif node_type == "host":
                noeud = Host(node_id, capacite)
            else:
                print("  ⚠️  Type invalide, nœud créé comme host par défaut.")
                noeud = Host(node_id, capacite)

            graph.ajouter_noeud(noeud)
            print(f"  ✅ Nœud '{node_id}' ajouté !")

        if not graph.noeuds:
            raise ReseauVideError()

        nb_liens = int(saisir_nombre("\nCombien de liens voulez-vous créer ? ", int))

        for i in range(nb_liens):
            print(f"\nLien {i + 1} :")
            source = input("  Source : ").strip()
            destination = input("  Destination : ").strip()

            if source not in graph.noeuds:
                raise NoeudInexistantError(source)
            if destination not in graph.noeuds:
                raise NoeudInexistantError(destination)

            bande_passante = saisir_nombre("  Bande passante (Mbps) : ")
            latence = saisir_nombre("  Latence (ms) : ")

            lien = NetworkLink(source, destination, bande_passante, latence)
            graph.ajouter_lien(lien)
            print(f"  ✅ Lien {source} → {destination} ajouté !")

        print("\n✅ Réseau créé avec succès !")
        return graph

    except NoeudInexistantError as e:
        print(f"\n❌ Erreur : {e}")
        return None
    except ReseauVideError as e:
        print(f"\n❌ Erreur : {e}")
        return None


def main():
    graph = None
    simulator = None
    reporter = None
    db = DatabaseManager()

    while True:
        choix = afficher_menu()

        if choix == "1":
            graph = creer_reseau()
            if graph:
                router = DijkstraRouter(graph)
                simulator = Simulator(graph, router)
                reporter = ReportGenerator(simulator)

        elif choix == "2":
            try:
                if simulator is None:
                    raise ReseauVideError()

                print("\nNœuds disponibles :")
                for node_id, noeud in graph.noeuds.items():
                    print(f"  - {node_id} ({noeud.node_type})")

                source = input("\nNœud source : ").strip()
                destination = input("Nœud destination : ").strip()

                if source not in graph.noeuds:
                    raise NoeudInexistantError(source)
                if destination not in graph.noeuds:
                    raise NoeudInexistantError(destination)

                chemin = DijkstraRouter(graph).find_path(source, destination)
                if not chemin:
                    raise CheminInexistantError(source, destination)

                nb_ticks = int(saisir_nombre("Nombre de ticks : ", int))
                nb_paquets = int(saisir_nombre("Nombre de paquets par tick : ", int))

                for _ in range(nb_ticks):
                    simulator.injecter_paquets(source, destination, nb_paquets)
                    simulator.executer_tick()

                stats = simulator.get_statistiques()
                goulots = simulator.get_goulots()
                sim_id = db.sauvegarder_simulation(stats, goulots)
                print(f"\n✅ Simulation terminée ! (sauvegardée en base — ID #{sim_id})")

            except (ReseauVideError, NoeudInexistantError, CheminInexistantError) as e:
                print(f"\n❌ Erreur : {e}")

        elif choix == "3":
            try:
                if reporter is None:
                    raise ReseauVideError()
                print(reporter.generer_rapport_texte())
            except ReseauVideError as e:
                print(f"\n❌ Erreur : {e}")

        elif choix == "4":
            try:
                if reporter is None:
                    raise ReseauVideError()
                fichier = reporter.exporter_csv()
                print(f"\n✅ Rapport exporté : {fichier}")
            except ReseauVideError as e:
                print(f"\n❌ Erreur : {e}")

        elif choix == "5":
            try:
                if graph is None:
                    raise ReseauVideError()
                graph.sauvegarder_json("configs/sample_network.json")
                print("\n✅ Réseau sauvegardé !")
            except ReseauVideError as e:
                print(f"\n❌ Erreur : {e}")

        elif choix == "6":
            try:
                import os
                if not os.path.exists("configs/sample_network.json"):
                    raise FichierIntrouvableError("configs/sample_network.json")
                graph = NetworkGraph()
                graph.charger_json("configs/sample_network.json")
                router = DijkstraRouter(graph)
                simulator = Simulator(graph, router)
                reporter = ReportGenerator(simulator)
                print("\n✅ Réseau chargé !")
            except FichierIntrouvableError as e:
                print(f"\n❌ Erreur : {e}")
            except Exception as e:
                print(f"\n❌ Erreur lors du chargement : {e}")

        elif choix == "7":
            print(db.afficher_historique())

        elif choix == "0":
            print("\nAu revoir ! 👋")
            break

        else:
            print("\n⚠️  Choix invalide !")


if __name__ == "__main__":
    main()
