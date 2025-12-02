"""
Tests unitaires complets pour le gestionnaire de tâches.

Ce module contient des tests pour:
- Les méthodes de TaskService (ajouter, lister, basculer, supprimer)
- La logique métier isolée (mock du stockage)
- Les cas d'erreur (ID introuvable)
- Les cas nominaux et les edge cases

Tests: pytest test_app.py -v
Auteur : Guillaume M.
"""

import pytest
from unittest.mock import patch, MagicMock
from app import TaskService, Task, TaskNotFoundError


class TestTaskServiceAjouter:
    """Tests pour la méthode ajouter_tache."""
    
    def setup_method(self):
        """Initialise un nouveau service avant chaque test."""
        self.service = TaskService()
    
    def test_ajouter_tache_retourne_tache_avec_id_incremente(self):
        """
        ✓ Vérifie que ajouter_tache retourne une Task avec un ID unique.
        ✓ Vérifie que l'ID s'incrémente correctement.
        """
        # Arrange: service vide
        assert self.service.nombre_taches() == 0
        
        # Act: ajouter une tâche
        task1 = self.service.ajouter_tache("Première tâche")
        task2 = self.service.ajouter_tache("Deuxième tâche")
        
        # Assert: vérifications claires
        assert task1.id == 1, "La première tâche doit avoir l'ID 1"
        assert task2.id == 2, "La deuxième tâche doit avoir l'ID 2"
        assert task1.title == "Première tâche"
        assert task2.title == "Deuxième tâche"
    
    def test_ajouter_tache_initialise_done_a_false(self):
        """
        ✓ Vérifie que une nouvelle tâche a le statut 'done' à False par défaut.
        """
        # Arrange & Act
        task = self.service.ajouter_tache("Ma tâche")
        
        # Assert
        assert task.done is False, "Une nouvelle tâche doit être non-complétée"
    
    def test_ajouter_tache_augmente_le_nombre_de_taches(self):
        """
        ✓ Vérifie que chaque ajout augmente le nombre total de tâches.
        """
        # Arrange
        assert self.service.nombre_taches() == 0
        
        # Act & Assert à chaque étape
        self.service.ajouter_tache("Task 1")
        assert self.service.nombre_taches() == 1
        
        self.service.ajouter_tache("Task 2")
        assert self.service.nombre_taches() == 2
        
        self.service.ajouter_tache("Task 3")
        assert self.service.nombre_taches() == 3


class TestTaskServiceLister:
    """Tests pour la méthode lister_taches."""
    
    def setup_method(self):
        """Initialise un nouveau service avant chaque test."""
        self.service = TaskService()
    
    def test_lister_taches_retourne_liste_vide_initialement(self):
        """
        ✓ Vérifie que lister_taches retourne une liste vide au démarrage.
        """
        # Act
        tasks = self.service.lister_taches()
        
        # Assert
        assert isinstance(tasks, list), "lister_taches doit retourner une liste"
        assert len(tasks) == 0, "La liste doit être vide initialement"
    
    def test_lister_taches_retourne_toutes_les_taches_ajoutees(self):
        """
        ✓ Vérifie que lister_taches retourne toutes les tâches ajoutées.
        ✓ Vérifie que l'ordre est préservé.
        """
        # Arrange
        self.service.ajouter_tache("Tâche Alpha")
        self.service.ajouter_tache("Tâche Beta")
        self.service.ajouter_tache("Tâche Gamma")
        
        # Act
        tasks = self.service.lister_taches()
        
        # Assert
        assert len(tasks) == 3, "Doit retourner les 3 tâches ajoutées"
        assert tasks[0].title == "Tâche Alpha", "L'ordre doit être préservé"
        assert tasks[1].title == "Tâche Beta"
        assert tasks[2].title == "Tâche Gamma"
    
    def test_lister_taches_retourne_copie_de_la_liste(self):
        """
        ✓ Vérifie que lister_taches retourne une copie (pas la référence originale).
        """
        # Arrange
        self.service.ajouter_tache("Tâche")
        tasks_copy = self.service.lister_taches()
        
        # Act: modifier la liste retournée
        tasks_copy.clear()
        
        # Assert: la liste originale doit être intacte
        original_tasks = self.service.lister_taches()
        assert len(original_tasks) == 1, "La liste originale doit rester inchangée"


class TestTaskServiceBasculer:
    """Tests pour la méthode etat_tache (toggle)."""
    
    def setup_method(self):
        """Initialise un nouveau service avant chaque test."""
        self.service = TaskService()
    
    def test_basculer_tache_change_done_de_false_a_true(self):
        """
        ✓ Vérifie que basculer une tâche change son état de False à True.
        """
        # Arrange
        task = self.service.ajouter_tache("Tâche à faire")
        assert task.done is False
        
        # Act
        toggled = self.service.etat_tache(task.id)
        
        # Assert
        assert toggled.done is True, "L'état doit passer à True après basculement"
    
    def test_basculer_tache_change_done_de_true_a_false(self):
        """
        ✓ Vérifie que basculer à nouveau ramène l'état à False.
        """
        # Arrange
        task = self.service.ajouter_tache("Tâche")
        self.service.etat_tache(task.id)
        assert task.done is True
        
        # Act
        toggled = self.service.etat_tache(task.id)
        
        # Assert
        assert toggled.done is False, "L'état doit revenir à False"
    
    def test_basculer_tache_invalide_leve_exception_task_not_found(self):
        """
        ✓ Vérifie que basculer une tâche inexistante lève TaskNotFoundError.
        """
        # Act & Assert
        with pytest.raises(TaskNotFoundError) as exc_info:
            self.service.etat_tache(999)
        
        assert "Tâche avec l'ID 999 non trouvée" in str(exc_info.value), \
            "Le message d'erreur doit contenir l'ID et 'non trouvée'"
    
    def test_basculer_tache_retourne_la_tache_mise_a_jour(self):
        """
        ✓ Vérifie que etat_tache retourne la tâche mise à jour.
        """
        # Arrange
        original_task = self.service.ajouter_tache("Tâche")
        
        # Act
        returned_task = self.service.etat_tache(original_task.id)
        
        # Assert
        assert returned_task is original_task, \
            "etat_tache doit retourner la même instance de tâche"
        assert returned_task.done is True


class TestTaskServiceSupprimer:
    """Tests pour la méthode supprimer_tache."""
    
    def setup_method(self):
        """Initialise un nouveau service avant chaque test."""
        self.service = TaskService()
    
    def test_supprimer_tache_valide_retourne_true(self):
        """
        ✓ Vérifie que supprimer une tâche existante retourne True.
        """
        # Arrange
        task = self.service.ajouter_tache("Tâche à supprimer")
        
        # Act
        result = self.service.supprimer_tache(task.id)
        
        # Assert
        assert result is True, "La suppression doit retourner True"
    
    def test_supprimer_tache_invalide_retourne_false(self):
        """
        ✓ Vérifie que supprimer une tâche inexistante retourne False (pas d'exception).
        """
        # Act
        result = self.service.supprimer_tache(999)
        
        # Assert
        assert result is False, "La suppression d'une ID inexistante doit retourner False"
    
    def test_supprimer_tache_enleve_la_tache_de_la_liste(self):
        """
        ✓ Vérifie que la tâche est bien supprimée de la liste.
        """
        # Arrange
        task1 = self.service.ajouter_tache("Tâche 1")
        task2 = self.service.ajouter_tache("Tâche 2")
        task3 = self.service.ajouter_tache("Tâche 3")
        assert self.service.nombre_taches() == 3
        
        # Act
        self.service.supprimer_tache(task2.id)
        
        # Assert
        remaining = self.service.lister_taches()
        assert len(remaining) == 2, "Doit avoir 2 tâches restantes"
        assert task1 in remaining
        assert task2 not in remaining
        assert task3 in remaining
    
    def test_supprimer_tache_plusieurs_fois_ne_supprime_qu_une_fois(self):
        """
        ✓ Vérifie que supprimer la même tâche deux fois:
           - 1ère fois: retourne True
           - 2e fois: retourne False
        """
        # Arrange
        task = self.service.ajouter_tache("Tâche")
        
        # Act & Assert
        first_delete = self.service.supprimer_tache(task.id)
        assert first_delete is True, "Première suppression doit retourner True"
        
        second_delete = self.service.supprimer_tache(task.id)
        assert second_delete is False, "Deuxième suppression doit retourner False"


class TestTaskServiceIntegration:
    """Tests d'intégration combinant plusieurs méthodes."""
    
    def setup_method(self):
        """Initialise un nouveau service avant chaque test."""
        self.service = TaskService()
    
    def test_workflow_complet_add_toggle_delete(self):
        """
        ✓ Vérifie un workflow complet: ajouter → basculer → supprimer.
        """
        # Arrange & Act: Ajouter 2 tâches
        task1 = self.service.ajouter_tache("Faire du sport")
        task2 = self.service.ajouter_tache("Lire un livre")
        assert self.service.nombre_taches() == 2
        
        # Act: Basculer la première tâche
        self.service.etat_tache(task1.id)
        assert task1.done is True
        
        # Act: Supprimer la deuxième tâche
        result = self.service.supprimer_tache(task2.id)
        assert result is True
        
        # Assert: État final
        tasks = self.service.lister_taches()
        assert len(tasks) == 1
        assert tasks[0].id == task1.id
        assert tasks[0].done is True
    
    def test_scenario_multiple_tasks_lifecycle(self):
        """
        ✓ Vérifie le cycle de vie complet de plusieurs tâches.
        """
        # Ajouter des tâches
        tasks_created = [
            self.service.ajouter_tache(f"Tâche {i}") 
            for i in range(1, 6)
        ]
        assert self.service.nombre_taches() == 5
        
        # Marquer les tâches paires comme complétées
        for task in tasks_created:
            if task.id % 2 == 0:
                self.service.etat_tache(task.id)
        
        # Supprimer les tâches impaires
        for task in tasks_created:
            if task.id % 2 == 1:
                self.service.supprimer_tache(task.id)
        
        # Vérifier l'état final
        remaining = self.service.lister_taches()
        assert len(remaining) == 2
        for task in remaining:
            assert task.done is True, "Les tâches restantes doivent être complétées"


class TestTaskServiceEdgeCases:
    """Tests pour les cas limites et edge cases."""
    
    def setup_method(self):
        """Initialise un nouveau service avant chaque test."""
        self.service = TaskService()
    
    def test_ajouter_tache_avec_titre_vide_leve_exception(self):
        """
        ✓ Vérifie que ajouter une tâche avec un titre vide lève une exception.
        """
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.service.ajouter_tache("")
        
        assert "vide" in str(exc_info.value).lower()
    
    def test_ajouter_tache_avec_titre_whitespace_leve_exception(self):
        """
        ✓ Vérifie que ajouter une tâche avec juste des espaces lève une exception.
        """
        # Act & Assert
        with pytest.raises(ValueError):
            self.service.ajouter_tache("   ")
    
    def test_basculer_tache_avec_id_zero(self):
        """
        ✓ Vérifie que basculer une tâche avec ID 0 lève une exception.
        """
        # Act & Assert
        with pytest.raises(TaskNotFoundError):
            self.service.etat_tache(0)
    
    def test_basculer_tache_avec_id_negatif(self):
        """
        ✓ Vérifie que basculer une tâche avec ID négatif lève une exception.
        """
        # Act & Assert
        with pytest.raises(TaskNotFoundError):
            self.service.etat_tache(-1)
    
    def test_ajouter_100_taches(self):
        """
        ✓ Vérifie que le service peut gérer 100 tâches sans problème.
        """
        # Act
        for i in range(100):
            self.service.ajouter_tache(f"Tâche {i}")
        
        # Assert
        assert self.service.nombre_taches() == 100
        tasks = self.service.lister_taches()
        assert all(task.id > 0 for task in tasks)
        assert all(task.id <= 100 for task in tasks)


class TestTaskServiceMockStorage:
    """Tests avec mock du stockage pour isoler la logique métier."""
    
    def setup_method(self):
        """Initialise un nouveau service avant chaque test."""
        self.service = TaskService()
    
    @patch('storage.load_tasks')
    @patch('storage.save_tasks')
    def test_ajouter_tache_ne_appelle_pas_le_stockage_directement(
        self, mock_save, mock_load
    ):
        """
        ✓ Vérifie que ajouter_tache ne fait pas de I/O directement.
        ✓ Le stockage est isolé et testé séparément.
        """
        # Act
        self.service.ajouter_tache("Tâche test")
        
        # Assert: les mocks ne doivent pas être appelés
        mock_save.assert_not_called()
        mock_load.assert_not_called()
    
    def test_service_operations_restent_isolees_du_stockage(self):
        """
        ✓ Vérifie que les opérations du service restent indépendantes du stockage.
        ✓ Les tâches sont dans la mémoire du service, pas sur disque.
        """
        # Arrange
        task1 = self.service.ajouter_tache("Tâche 1")
        task2 = self.service.ajouter_tache("Tâche 2")
        
        # Act: Tous les changements sont en mémoire
        self.service.etat_tache(task1.id)
        self.service.supprimer_tache(task2.id)
        
        # Assert: Le service a l'état correct
        tasks = self.service.lister_taches()
        assert len(tasks) == 1
        assert tasks[0].done is True
        
        # Note: Sans appel à save_tasks, les données ne sont pas persistées


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])