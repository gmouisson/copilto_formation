"""
Module contenant les modèles de données pour le gestionnaire de tâches.
"""

from typing import Optional, List
from dataclasses import dataclass


@dataclass
class Task:
    """
    Représente une tâche individuelle.
    
    Attributs:
        id (int): Identifiant unique de la tâche.
        title (str): Titre descriptif de la tâche.
        done (bool): Statut de complétion de la tâche. Par défaut, False.
    
    Exemple:
        >>> task = Task(1, "Acheter du lait")
        >>> print(task.title)
        Acheter du lait
        >>> print(task.done)
        False
    """
    id: int
    title: str
    done: bool = False

    def __repr__(self) -> str:
        """Représentation lisible de la tâche."""
        status = "✓ DONE" if self.done else "○ NOT DONE"
        return f"[{self.id}] {self.title} - {status}"


class TaskNotFoundError(Exception):
    """Exception levée quand une tâche n'est pas trouvée."""
    pass


class TaskService:
    """
    Service de gestion des tâches avec opérations CRUD.
    
    Gère la création, lecture, mise à jour et suppression des tâches.
    Responsabilités:
        - Créer des nouvelles tâches avec identifiants uniques
        - Récupérer toutes les tâches
        - Mettre à jour l'état d'une tâche
        - Supprimer une tâche
        - Trouver une tâche par son ID
    
    Exemple:
        >>> service = TaskService()
        >>> task1 = service.ajouter_tache("Acheter du lait")
        >>> task2 = service.ajouter_tache("Faire du sport")
        >>> print(len(service.lister_taches()))
        2
        >>> service.etat_tache(task1.id)
        >>> print(task1.done)
        True
        >>> service.supprimer_tache(task2.id)
        >>> print(len(service.lister_taches()))
        1
    """

    def __init__(self) -> None:
        """Initialise le service avec une liste vide et un compteur d'ID."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def ajouter_tache(self, title: str) -> Task:
        """
        Crée et ajoute une nouvelle tâche au service.
        
        Args:
            title (str): Le titre de la tâche à créer.
        
        Returns:
            Task: La tâche créée avec un identifiant unique.
        
        Raises:
            ValueError: Si le titre est vide.
        
        Exemple:
            >>> service = TaskService()
            >>> task = service.ajouter_tache("Ma première tâche")
            >>> print(task.id)
            1
            >>> print(task.title)
            Ma première tâche
        """
        if not title or not title.strip():
            raise ValueError("Le titre de la tâche ne peut pas être vide.")
        
        # Crée une nouvelle tâche avec l'ID actuel
        task = Task(id=self._next_id, title=title.strip())
        self._tasks.append(task)
        self._next_id += 1
        
        return task

    def lister_taches(self) -> List[Task]:
        """
        Récupère la liste complète de toutes les tâches.
        
        Returns:
            List[Task]: Une copie de la liste des tâches.
        
        Exemple:
            >>> service = TaskService()
            >>> service.ajouter_tache("Task 1")
            >>> service.ajouter_tache("Task 2")
            >>> tasks = service.lister_taches()
            >>> print(len(tasks))
            2
        """
        return self._tasks.copy()

    def obtenir_tache(self, task_id: int) -> Task:
        """
        Récupère une tâche spécifique par son ID.
        
        Args:
            task_id (int): L'identifiant de la tâche à récupérer.
        
        Returns:
            Task: La tâche correspondant à l'ID.
        
        Raises:
            TaskNotFoundError: Si aucune tâche ne correspond à cet ID.
        
        Exemple:
            >>> service = TaskService()
            >>> task = service.ajouter_tache("Ma tâche")
            >>> found = service.obtenir_tache(1)
            >>> print(found.title)
            Ma tâche
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        
        raise TaskNotFoundError(f"Tâche avec l'ID {task_id} non trouvée.")

    def etat_tache(self, task_id: int) -> Task:
        """
        Bascule l'état de complétion d'une tâche (terminée ↔ non-terminée).
        
        Args:
            task_id (int): L'identifiant de la tâche à modifier.
        
        Returns:
            Task: La tâche mise à jour.
        
        Raises:
            TaskNotFoundError: Si aucune tâche ne correspond à cet ID.
        
        Exemple:
            >>> service = TaskService()
            >>> task = service.ajouter_tache("Ma tâche")
            >>> print(task.done)
            False
            >>> service.etat_tache(task.id)
            >>> print(task.done)
            True
        """
        task = self.obtenir_tache(task_id)
        task.done = not task.done
        return task

    def supprimer_tache(self, task_id: int) -> bool:
        """
        Supprime définitivement une tâche du service.
        
        Args:
            task_id (int): L'identifiant de la tâche à supprimer.
        
        Returns:
            bool: True si la suppression a réussi, False si la tâche n'existe pas.
        
        Exemple:
            >>> service = TaskService()
            >>> task = service.ajouter_tache("Ma tâche")
            >>> service.supprimer_tache(task.id)
            True
            >>> service.supprimer_tache(999)
            False
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return True
        
        return False

    def obtenir_taches_en_cours(self) -> List[Task]:
        """
        Récupère toutes les tâches non-terminées.
        
        Returns:
            List[Task]: Liste des tâches non-terminées.
        
        Exemple:
            >>> service = TaskService()
            >>> t1 = service.ajouter_tache("Task 1")
            >>> t2 = service.ajouter_tache("Task 2")
            >>> service.etat_tache(t1.id)
            >>> en_cours = service.obtenir_taches_en_cours()
            >>> print(len(en_cours))
            1
        """
        return [task for task in self._tasks if not task.done]

    def obtenir_taches_terminees(self) -> List[Task]:
        """
        Récupère toutes les tâches terminées.
        
        Returns:
            List[Task]: Liste des tâches terminées.
        
        Exemple:
            >>> service = TaskService()
            >>> t1 = service.ajouter_tache("Task 1")
            >>> service.etat_tache(t1.id)
            >>> terminees = service.obtenir_taches_terminees()
            >>> print(len(terminees))
            1
        """
        return [task for task in self._tasks if task.done]

    def nombre_taches(self) -> int:
        """
        Retourne le nombre total de tâches.
        
        Returns:
            int: Le nombre de tâches dans le service.
        """
        return len(self._tasks)

    def nombre_taches_en_cours(self) -> int:
        """Retourne le nombre de tâches non-terminées."""
        return len(self.obtenir_taches_en_cours())

    def nombre_taches_terminees(self) -> int:
        """Retourne le nombre de tâches terminées."""
        return len(self.obtenir_taches_terminees())

    def reinitialiser(self) -> None:
        """
        Réinitialise complètement le service (supprime toutes les tâches).
        
        Utile pour les tests ou pour recommencer de zéro.
        """
        self._tasks.clear()
        self._next_id = 1


# Exemple d'utilisation
if __name__ == "__main__":
    # Créer un service
    service = TaskService()
    
    # Ajouter des tâches
    print("=== Ajout de tâches ===")
    task1 = service.ajouter_tache("Acheter du lait")
    task2 = service.ajouter_tache("Faire du sport")
    task3 = service.ajouter_tache("Terminer le projet")
    print(f"✓ {task1}")
    print(f"✓ {task2}")
    print(f"✓ {task3}")
    
    # Lister toutes les tâches
    print("\n=== Toutes les tâches ===")
    for task in service.lister_taches():
        print(f"  {task}")
    
    # Marquer une tâche comme terminée
    print("\n=== Marquer task1 comme terminée ===")
    service.etat_tache(task1.id)
    print(f"✓ {task1}")
    
    # Afficher les statistiques
    print("\n=== Statistiques ===")
    print(f"Total: {service.nombre_taches()}")
    print(f"En cours: {service.nombre_taches_en_cours()}")
    print(f"Terminées: {service.nombre_taches_terminees()}")
    
    # Supprimer une tâche
    print("\n=== Suppression de task2 ===")
    service.supprimer_tache(task2.id)
    print("✓ Supprimée")
    
    # Lister les tâches restantes
    print("\n=== Tâches restantes ===")
    for task in service.lister_taches():
        print(f"  {task}")

