"""
Tests unitaires pour l'API Task Manager.
Utilise pytest pour tester tous les endpoints et la logique métier.
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import app, TaskService


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def client():
    """Crée un client de test FastAPI."""
    return TestClient(app)


@pytest.fixture
def task_service():
    """Crée une instance du service de tâches."""
    return TaskService()


# ============================================================================
# Tests du Service de Tâches
# ============================================================================

class TestTaskService:
    """Tests du service de gestion des tâches."""
    
    def test_creer_tache(self, task_service):
        """Test la création d'une tâche."""
        from main import TaskCreate
        
        task_create = TaskCreate(title="Ma tâche test")
        task = task_service.creer_tache(task_create)
        
        assert task.id == 1
        assert task.title == "Ma tâche test"
        assert task.done is False
    
    def test_obtenir_toutes_les_taches(self, task_service):
        """Test la récupération de toutes les tâches."""
        from main import TaskCreate
        
        task_service.creer_tache(TaskCreate(title="Task 1"))
        task_service.creer_tache(TaskCreate(title="Task 2"))
        
        tasks = task_service.obtenir_toutes_les_taches()
        assert len(tasks) == 2
    
    def test_obtenir_tache_par_id(self, task_service):
        """Test la récupération d'une tâche par son ID."""
        from main import TaskCreate
        
        created_task = task_service.creer_tache(TaskCreate(title="Test"))
        retrieved_task = task_service.obtenir_tache(created_task.id)
        
        assert retrieved_task.title == "Test"
    
    def test_obtenir_tache_inexistante(self, task_service):
        """Test la récupération d'une tâche inexistante."""
        with pytest.raises(ValueError):
            task_service.obtenir_tache(999)
    
    def test_basculer_tache(self, task_service):
        """Test le basculement d'état d'une tâche."""
        from main import TaskCreate
        
        task = task_service.creer_tache(TaskCreate(title="Test"))
        assert task.done is False
        
        toggled = task_service.basculer_tache(task.id)
        assert toggled.done is True
        
        toggled = task_service.basculer_tache(task.id)
        assert toggled.done is False
    
    def test_supprimer_tache(self, task_service):
        """Test la suppression d'une tâche."""
        from main import TaskCreate
        
        task = task_service.creer_tache(TaskCreate(title="Test"))
        task_service.supprimer_tache(task.id)
        
        with pytest.raises(ValueError):
            task_service.obtenir_tache(task.id)


# ============================================================================
# Tests des Endpoints API
# ============================================================================

class TestTaskAPI:
    """Tests des endpoints de l'API."""
    
    def test_get_root(self, client):
        """Test l'endpoint racine."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "endpoints" in data
    
    def test_post_task_create(self, client):
        """Test la création d'une tâche via l'API."""
        response = client.post(
            "/tasks",
            json={"title": "Acheter du lait"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Acheter du lait"
        assert data["done"] is False
        assert data["id"] == 1
    
    def test_get_all_tasks(self, client):
        """Test la récupération de toutes les tâches."""
        # Créer quelques tâches
        client.post("/tasks", json={"title": "Task 1"})
        client.post("/tasks", json={"title": "Task 2"})
        
        response = client.get("/tasks")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_get_tasks_filter_by_done(self, client):
        """Test le filtrage des tâches par statut."""
        # Créer des tâches
        response1 = client.post("/tasks", json={"title": "Task 1"})
        task_id_1 = response1.json()["id"]
        
        response2 = client.post("/tasks", json={"title": "Task 2"})
        task_id_2 = response2.json()["id"]
        
        # Marquer une comme terminée
        client.patch(f"/tasks/{task_id_1}/toggle")
        
        # Filtrer par done=true
        response = client.get("/tasks?done=true")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        
        # Filtrer par done=false
        response = client.get("/tasks?done=false")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
    
    def test_get_single_task(self, client):
        """Test la récupération d'une tâche spécifique."""
        # Créer une tâche
        create_response = client.post("/tasks", json={"title": "Test Task"})
        task_id = create_response.json()["id"]
        
        # Récupérer la tâche
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Task"
    
    def test_get_task_not_found(self, client):
        """Test la récupération d'une tâche inexistante."""
        response = client.get("/tasks/999")
        assert response.status_code == 404
    
    def test_patch_toggle_task(self, client):
        """Test le basculement d'une tâche."""
        # Créer une tâche
        create_response = client.post("/tasks", json={"title": "Test Task"})
        task_id = create_response.json()["id"]
        
        # Basculer
        response = client.patch(f"/tasks/{task_id}/toggle")
        assert response.status_code == 200
        data = response.json()
        assert data["done"] is True
    
    def test_patch_update_task(self, client):
        """Test la mise à jour d'une tâche."""
        # Créer une tâche
        create_response = client.post("/tasks", json={"title": "Ancien titre"})
        task_id = create_response.json()["id"]
        
        # Mettre à jour
        response = client.patch(
            f"/tasks/{task_id}",
            json={"title": "Nouveau titre", "done": True}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Nouveau titre"
        assert data["done"] is True
    
    def test_delete_task(self, client):
        """Test la suppression d'une tâche."""
        # Créer une tâche
        create_response = client.post("/tasks", json={"title": "À supprimer"})
        task_id = create_response.json()["id"]
        
        # Supprimer
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204
        
        # Vérifier qu'elle n'existe plus
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 404
    
    def test_get_statistics(self, client):
        """Test le endpoint des statistiques."""
        # Créer des tâches
        response1 = client.post("/tasks", json={"title": "Task 1"})
        task_id_1 = response1.json()["id"]
        
        response2 = client.post("/tasks", json={"title": "Task 2"})
        
        # Marquer une comme terminée
        client.patch(f"/tasks/{task_id_1}/toggle")
        
        # Récupérer les stats
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert data["terminees"] == 1
        assert data["en_cours"] == 1


# ============================================================================
# Tests de Validation
# ============================================================================

class TestValidation:
    """Tests de validation des données."""
    
    def test_title_required(self, client):
        """Test que le titre est requis."""
        response = client.post("/tasks", json={})
        assert response.status_code == 422  # Validation error
    
    def test_title_min_length(self, client):
        """Test la longueur minimale du titre."""
        response = client.post("/tasks", json={"title": ""})
        assert response.status_code == 422
    
    def test_title_max_length(self, client):
        """Test la longueur maximale du titre."""
        long_title = "a" * 300
        response = client.post("/tasks", json={"title": long_title})
        assert response.status_code == 422
    
    def test_invalid_task_id(self, client):
        """Test un ID de tâche invalide."""
        response = client.get("/tasks/invalid")
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
