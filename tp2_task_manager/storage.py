"""
Module de persistance pour stocker et charger les tâches en JSON.

Ce module gère la sérialisation/désérialisation des tâches
et l'interaction avec le système de fichiers.
"""

import json
import os
from typing import List, Dict, Any


TASKS_FILE: str = "tasks.json"


def load_tasks() -> List[Dict[str, Any]]:
    """
    Charge toutes les tâches depuis le fichier JSON de stockage.
    
    Retourne une liste vide si le fichier n'existe pas.
    
    Returns:
        List[Dict[str, Any]]: Liste des tâches au format dictionnaire.
                              Format: [{"id": 1, "title": "...", "done": False}, ...]
    
    Raises:
        json.JSONDecodeError: Si le fichier JSON est malformé.
        PermissionError: Si le fichier ne peut pas être lu.
    
    Exemple:
        >>> tasks = load_tasks()
        >>> print(len(tasks))
        0  # Au premier démarrage
    """
    if not os.path.exists(TASKS_FILE):
        # Fichier n'existe pas encore: retourner liste vide
        return []
    
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            # Valider que c'est une liste
            if not isinstance(data, list):
                print(f"⚠️  Avertissement: {TASKS_FILE} n'est pas un JSON valide (attendu une liste)")
                return []
            return data
    except json.JSONDecodeError as e:
        print(f"❌ Erreur: Le fichier {TASKS_FILE} contient du JSON invalide: {e}")
        return []


def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """
    Sauvegarde la liste des tâches dans le fichier JSON.
    
    Crée ou remplace le fichier si nécessaire.
    Formate le JSON avec indentation pour faciliter la lecture.
    
    Args:
        tasks (List[Dict[str, Any]]): Liste des tâches à sauvegarder.
                                     Format: [{"id": 1, "title": "...", "done": False}, ...]
    
    Raises:
        PermissionError: Si le fichier ne peut pas être écrit.
        TypeError: Si les données ne sont pas sérialisables en JSON.
    
    Exemple:
        >>> tasks = [{"id": 1, "title": "Ma tâche", "done": False}]
        >>> save_tasks(tasks)
        # Le fichier tasks.json est créé/mis à jour
    """
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)
    except PermissionError:
        print(f"❌ Erreur: Impossible d'accéder au fichier {TASKS_FILE} (permission refusée)")
        raise
    except TypeError as e:
        print(f"❌ Erreur: Les données ne peuvent pas être sérialisées en JSON: {e}")
        raise


def clear_storage() -> None:
    """
    Supprime le fichier de stockage des tâches.
    
    Utile pour réinitialiser complètement l'application ou pour les tests.
    N'affiche aucune erreur si le fichier n'existe pas.
    """
    if os.path.exists(TASKS_FILE):
        try:
            os.remove(TASKS_FILE)
            print(f"✅ Fichier {TASKS_FILE} supprimé")
        except PermissionError:
            print(f"❌ Erreur: Impossible de supprimer {TASKS_FILE}")
            raise


def fichier_existe() -> bool:
    """
    Vérifie si le fichier de stockage existe.
    
    Returns:
        bool: True si le fichier existe, False sinon.
    """
    return os.path.exists(TASKS_FILE)


def chemin_fichier() -> str:
    """
    Retourne le chemin absolu du fichier de stockage.
    
    Returns:
        str: Chemin absolu du fichier.
    
    Exemple:
        >>> path = chemin_fichier()
        >>> print(path)
        /path/to/tasks.json
    """
    return os.path.abspath(TASKS_FILE)


def taille_fichier() -> int:
    """
    Retourne la taille du fichier de stockage en octets.
    
    Returns:
        int: Taille en octets, ou 0 si le fichier n'existe pas.
    """
    if not fichier_existe():
        return 0
    return os.path.getsize(TASKS_FILE)


# Exemple d'utilisation
if __name__ == "__main__":
    print("Module de stockage des tâches")
    print(f"Fichier: {chemin_fichier()}")
    print(f"Existe: {fichier_existe()}")
    print(f"Taille: {taille_fichier()} octets")
    
    # Charger les tâches existantes
    tasks = load_tasks()
    print(f"Tâches chargées: {len(tasks)}")
    
    if tasks:
        for task in tasks:
            print(f"  - [{task['id']}] {task['title']} - {'✓ DONE' if task['done'] else '○ NOT DONE'}")
