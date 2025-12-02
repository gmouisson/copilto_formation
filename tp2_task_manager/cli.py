"""
Interface en ligne de commande (CLI) pour le gestionnaire de tâches.
Utilise argparse pour gérer les commandes: add, list, toggle, delete.
"""

import argparse
import sys
from typing import Optional

from app import Task, TaskService, TaskNotFoundError
from storage import load_tasks, save_tasks


class TaskCLI:
    """
    Gestionnaire d'interface CLI pour les tâches.
    
    Responsabilités:
        - Parser les arguments de la ligne de commande
        - Afficher les tâches de manière lisible
        - Gérer les erreurs utilisateur
        - Persister les données
    """

    def __init__(self) -> None:
        """Initialise le CLI avec le service et charge les données persistantes."""
        self.service: TaskService = TaskService()
        self._charger_donnees_persistantes()

    def _charger_donnees_persistantes(self) -> None:
        """
        Charge les tâches depuis le stockage JSON.
        Met à jour l'ID suivant selon la plus haute tâche existante.
        """
        tasks_data = load_tasks()
        for task_dict in tasks_data:
            task = Task(**task_dict)
            self.service._tasks.append(task)
            # Met à jour le prochain ID
            if task.id >= self.service._next_id:
                self.service._next_id = task.id + 1

    def _sauvegarder_donnees(self) -> None:
        """Persiste toutes les tâches actuelles dans le fichier JSON."""
        tasks_data = [
            {"id": task.id, "title": task.title, "done": task.done}
            for task in self.service.lister_taches()
        ]
        save_tasks(tasks_data)

    def afficher_tache(self, task: Task) -> None:
        """Affiche une tâche avec un format lisible."""
        print(f"  {task}")

    def afficher_statistiques(self) -> None:
        """Affiche les statistiques des tâches."""
        total = self.service.nombre_taches()
        en_cours = self.service.nombre_taches_en_cours()
        terminees = self.service.nombre_taches_terminees()
        
        print(f"\n📊 Statistiques: Total={total} | En cours={en_cours} | Terminées={terminees}")

    def commande_ajouter(self, title: str) -> None:
        """
        Ajoute une nouvelle tâche.
        
        Args:
            title (str): Le titre de la tâche.
        """
        try:
            task = self.service.ajouter_tache(title)
            print(f"✅ Tâche ajoutée: {task}")
            self.afficher_statistiques()
        except ValueError as e:
            print(f"❌ Erreur: {e}")
            sys.exit(1)

    def commande_lister(self) -> None:
        """Liste toutes les tâches."""
        tasks = self.service.lister_taches()
        
        if not tasks:
            print("📭 Aucune tâche. Commencez par en ajouter une!")
            return
        
        print("\n📋 Toutes les tâches:")
        for task in tasks:
            self.afficher_tache(task)
        
        self.afficher_statistiques()

    def commande_basculer(self, task_id: int) -> None:
        """
        Bascule l'état d'une tâche.
        
        Args:
            task_id (int): L'ID de la tâche à modifier.
        """
        try:
            task = self.service.etat_tache(task_id)
            status = "✅ terminée" if task.done else "⏳ remise en cours"
            print(f"🔄 Tâche {status}: {task}")
            self.afficher_statistiques()
        except TaskNotFoundError as e:
            print(f"❌ Erreur: {e}")
            sys.exit(1)

    def commande_supprimer(self, task_id: int) -> None:
        """
        Supprime une tâche.
        
        Args:
            task_id (int): L'ID de la tâche à supprimer.
        """
        if self.service.supprimer_tache(task_id):
            print(f"🗑️  Tâche avec l'ID {task_id} supprimée.")
            self.afficher_statistiques()
        else:
            print(f"❌ Erreur: Tâche avec l'ID {task_id} non trouvée.")
            sys.exit(1)

    def commande_taches_en_cours(self) -> None:
        """Liste uniquement les tâches non-terminées."""
        tasks = self.service.obtenir_taches_en_cours()
        
        if not tasks:
            print("🎉 Aucune tâche en cours. Bien joué!")
            return
        
        print("\n⏳ Tâches en cours:")
        for task in tasks:
            self.afficher_tache(task)
        
        self.afficher_statistiques()

    def commande_taches_terminees(self) -> None:
        """Liste uniquement les tâches terminées."""
        tasks = self.service.obtenir_taches_terminees()
        
        if not tasks:
            print("📭 Aucune tâche terminée.")
            return
        
        print("\n✅ Tâches terminées:")
        for task in tasks:
            self.afficher_tache(task)
        
        self.afficher_statistiques()

    def construire_parseur(self) -> argparse.ArgumentParser:
        """
        Construit le parseur argparse avec toutes les commandes.
        
        Returns:
            ArgumentParser: Le parseur configuré.
        """
        parser = argparse.ArgumentParser(
            description="📋 Gestionnaire de tâches CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Exemples d'utilisation:
  python cli.py add "Acheter du lait"
  python cli.py list
  python cli.py toggle 1
  python cli.py delete 1
  python cli.py done      (voir les tâches terminées)
  python cli.py pending   (voir les tâches en cours)
            """
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

        # Commande: add
        add_parser = subparsers.add_parser(
            "add",
            help="Ajouter une nouvelle tâche"
        )
        add_parser.add_argument(
            "title",
            type=str,
            help="Titre de la tâche"
        )

        # Commande: list
        subparsers.add_parser(
            "list",
            help="Lister toutes les tâches"
        )

        # Commande: toggle
        toggle_parser = subparsers.add_parser(
            "toggle",
            help="Basculer l'état d'une tâche (terminée/non-terminée)"
        )
        toggle_parser.add_argument(
            "id",
            type=int,
            help="ID de la tâche à modifier"
        )

        # Commande: delete
        delete_parser = subparsers.add_parser(
            "delete",
            help="Supprimer une tâche"
        )
        delete_parser.add_argument(
            "id",
            type=int,
            help="ID de la tâche à supprimer"
        )

        # Commande: done
        subparsers.add_parser(
            "done",
            help="Lister les tâches terminées"
        )

        # Commande: pending
        subparsers.add_parser(
            "pending",
            help="Lister les tâches en cours"
        )

        return parser

    def executer(self) -> None:
        """
        Exécute le CLI en traitant les arguments et en effectuant l'action appropriée.
        """
        parser = self.construire_parseur()
        args = parser.parse_args()

        # Si aucune commande spécifiée, afficher l'aide
        if not args.command:
            parser.print_help()
            return

        # Dispatcher vers la commande appropriée
        if args.command == "add":
            self.commande_ajouter(args.title)
        elif args.command == "list":
            self.commande_lister()
        elif args.command == "toggle":
            self.commande_basculer(args.id)
        elif args.command == "delete":
            self.commande_supprimer(args.id)
        elif args.command == "done":
            self.commande_taches_terminees()
        elif args.command == "pending":
            self.commande_taches_en_cours()

        # Sauvegarder les changements
        self._sauvegarder_donnees()


def main() -> None:
    """Point d'entrée principal du programme."""
    cli = TaskCLI()
    cli.executer()


if __name__ == "__main__":
    main()
