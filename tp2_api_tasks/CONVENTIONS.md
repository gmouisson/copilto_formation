# Conventions de Code - API Task Manager

## 📋 Vue d'ensemble

Ce document décrit les conventions appliquées au projet pour maintenir la cohérence, la qualité et la maintenabilité du code.

## 1. Conventions de Nommage

### 1.1 Fonctions et Méthodes
- **Convention**: `snake_case` en anglais
- **Verbes courants**: `get_`, `list_`, `create_`, `update_`, `delete_`, `toggle_`
- **Exemples**:
  ```python
  def get_by_id(self, task_id: int) -> Task
  def list_tasks(filter: Optional[bool]) -> List[Task]
  def create_task(task_data: TaskCreate) -> Task
  def update_task(task_id: int, updates: TaskUpdate) -> Task
  def delete_task(task_id: int) -> None
  def toggle_task(task_id: int) -> Task
  ```

### 1.2 Endpoints API
- **Convention**: `snake_case` en minuscules
- **Format**: `/ressource`, `/ressource/{id}`, `/ressource/{id}/action`
- **Exemples**:
  ```
  GET    /tasks              # Lister toutes les tâches
  POST   /tasks              # Créer une tâche
  GET    /tasks/{task_id}    # Récupérer une tâche
  PATCH  /tasks/{task_id}    # Mettre à jour une tâche
  PATCH  /tasks/{task_id}/toggle  # Basculer l'état
  DELETE /tasks/{task_id}    # Supprimer une tâche
  GET    /stats              # Statistiques
  ```

### 1.3 Variables et Paramètres
- **Convention**: `snake_case` en anglais
- **Préfixe `_` pour les privés**: `_tasks`, `_next_id`
- **Exemples**:
  ```python
  task_id: int
  task_service: TaskService
  completion_percentage: float
  done_count: int
  pending_count: int
  ```

### 1.4 Classes et Modèles
- **Convention**: `PascalCase`
- **Exceptions suffixées par `Error`**: `TaskNotFoundError`, `TaskValidationError`
- **Modèles Pydantic**: `Task`, `TaskCreate`, `TaskUpdate`
- **Services**: `TaskService`
- **Exemples**:
  ```python
  class Task(BaseModel):
  class TaskCreate(BaseModel):
  class TaskService:
  class TaskNotFoundError(Exception):
  class TaskValidationError(Exception):
  ```

## 2. Gestion des Erreurs

### 2.1 Exceptions Personnalisées
Les exceptions métier doivent être explicites et hériter d'une classe personnalisée:

```python
class TaskNotFoundError(Exception):
    """Exception levée quand une tâche n'est pas trouvée."""
    pass

class TaskValidationError(Exception):
    """Exception levée en cas d'erreur de validation de tâche."""
    pass
```

### 2.2 Codes HTTP Standards
- `200 OK`: Succès (GET, PATCH)
- `201 Created`: Ressource créée (POST)
- `204 No Content`: Suppression réussie (DELETE)
- `400 Bad Request`: Erreur de validation
- `404 Not Found`: Ressource introuvable
- `422 Unprocessable Entity`: Erreur de validation Pydantic

### 2.3 Gestion dans les Endpoints
```python
@app.get("/tasks/{task_id}")
def get_task(task_id: int) -> Task:
    try:
        logger.info(f"Récupération de la tâche: ID={task_id}")
        return task_service.get_by_id(task_id)
    except TaskNotFoundError as e:
        logger.warning(f"Tâche non trouvée: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
```

## 3. Logging Structuré

### 3.1 Niveaux de Log
- **DEBUG**: Informations de débogage détaillées
- **INFO**: Événements normaux importants
- **WARNING**: Événements inhabituels ou potentiels problèmes
- **ERROR**: Erreurs sérieuses
- **CRITICAL**: Erreurs très graves

### 3.2 Format des Logs
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### 3.3 Exemples de Logs
```python
# INFO: Opérations réussies
logger.info(f"Tâche créée: ID={task.id}, Titre='{task.title}'")
logger.info(f"Récupération de la tâche: ID={task_id}")
logger.info(f"Mise à jour de la tâche: ID={task_id}, Changements=[...]")

# DEBUG: Informations détaillées
logger.debug(f"Récupération de {len(self._tasks)} tâches")
logger.debug(f"Aucune modification pour la tâche: ID={task_id}")

# WARNING: Situations inhabituelles
logger.warning(f"Tâche non trouvée: ID={task_id}")
logger.warning(f"Tentative de suppression de tâche inexistante: ID={task_id}")

# ERROR: Erreurs
logger.error(f"Erreur lors de la création de tâche: {str(e)}")
```

### 3.4 Contexte du Log
Les logs doivent inclure le contexte pertinent:
```python
# ✓ BON
logger.info(f"Tâche créée: ID={task.id}, Titre='{task.title}'")
logger.info(f"Filtre appliqué: {len(tasks)} tâches avec done={done}")
logger.info(f"Statistiques: total={total}, terminees={done_count}, en_cours={pending_count}, completion={completion_percentage}%")

# ✗ MAUVAIS
logger.info("Tâche créée")  # Pas d'informations pertinentes
logger.info(f"Valeur: {task_id}")  # Manque de contexte
```

## 4. Documentation

### 4.1 Docstrings
Tous les modules, classes et fonctions publiques doivent avoir une docstring:

```python
def get_by_id(self, task_id: int) -> Task:
    """
    Récupère une tâche par son ID.
    
    Args:
        task_id (int): L'ID de la tâche à récupérer.
        
    Returns:
        Task: La tâche trouvée.
        
    Raises:
        TaskNotFoundError: Si la tâche n'existe pas.
    """
    ...
```

### 4.2 Commentaires
Les commentaires doivent expliquer le **pourquoi**, pas le **quoi**:

```python
# ✓ BON
# Réinitialiser le service global avant chaque test pour éviter les effets de bord
global_service._tasks.clear()
global_service._next_id = 1

# ✗ MAUVAIS
# Effacer les tâches et réinitialiser l'ID
global_service._tasks.clear()
global_service._next_id = 1
```

## 5. Structure du Code

### 5.1 Ordre des Imports
```python
# 1. Imports standard
import logging
from typing import List, Optional

# 2. Imports tiers
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

# 3. Imports locaux
from main import TaskService
```

### 5.2 Organisation du Fichier
```python
# 1. Module docstring
# 2. Imports
# 3. Configuration (logging, constantes)
# 4. Exceptions personnalisées
# 5. Modèles Pydantic
# 6. Services/Logique métier
# 7. Application FastAPI
# 8. Middleware
# 9. Endpoints (routes)
# 10. Point d'entrée (if __name__ == "__main__")
```

### 5.3 Séparation des Sections
Utiliser des commentaires de section:
```python
# ============================================================================
# Configuration des Logs
# ============================================================================

# ============================================================================
# Exceptions Personnalisées
# ============================================================================

# ============================================================================
# Modèles Pydantic
# ============================================================================

# ============================================================================
# Service de Tâches (Logique Métier)
# ============================================================================
```

## 6. Tests

### 6.1 Nommage des Tests
- Convention: `test_<action>_<context>` ou `test_<action>_<result>`
- Exemples:
  ```python
  def test_create_task(self):
  def test_create_task_with_description(self):
  def test_get_task_not_found(self):
  def test_update_task_title(self):
  def test_delete_task_verify_deleted(self):
  ```

### 6.2 Organisation des Tests
```python
class TestTaskService:
    """Tests du service de gestion des tâches."""

class TestTaskAPI:
    """Tests des endpoints de l'API."""

class TestValidation:
    """Tests de validation des données."""

class TestIntegration:
    """Tests d'intégration complets."""
```

## 7. Type Hints

### 7.1 Utilisation Obligatoire
Tous les paramètres et valeurs de retour doivent avoir des type hints:

```python
# ✓ BON
def get_by_id(self, task_id: int) -> Task:
    tasks: List[Task] = self.get_all()
    done_count: int = sum(1 for task in tasks if task.done)
    
# ✗ MAUVAIS
def get_by_id(self, task_id):
    tasks = self.get_all()
    done_count = sum(1 for task in tasks if task.done)
```

### 7.2 Imports de Types
```python
from typing import List, Optional, Dict, Tuple
```

## 8. Validation et Constantes

### 8.1 Constantes
Les constantes doivent être en MAJUSCULES_AVEC_UNDERSCORES:

```python
MAX_TITLE_LENGTH = 255
MIN_TITLE_LENGTH = 1
DEFAULT_DONE_STATUS = False
API_VERSION = "1.0.0"
```

### 8.2 Validation Pydantic
```python
class Task(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="...")
    done: bool = Field(default=False, description="...")
```

## 9. Exemple Complet

```python
"""Module de gestion des tâches."""

import logging
from fastapi import FastAPI, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class TaskNotFoundError(Exception):
    """Exception levée quand une tâche n'est pas trouvée."""
    pass

class Task(BaseModel):
    """Modèle représentant une tâche."""
    id: int = Field(..., description="Identifiant unique")
    title: str = Field(..., min_length=1, max_length=255)
    done: bool = Field(default=False)
    description: Optional[str] = Field(default=None)

class TaskService:
    """Service de gestion des tâches."""
    
    def __init__(self) -> None:
        """Initialise le service."""
        self._tasks: List[Task] = []
        self._next_id: int = 1
        logger.info("Service de tâches initialisé")
    
    def get_by_id(self, task_id: int) -> Task:
        """
        Récupère une tâche par son ID.
        
        Args:
            task_id: L'ID de la tâche.
            
        Returns:
            La tâche trouvée.
            
        Raises:
            TaskNotFoundError: Si la tâche n'existe pas.
        """
        for task in self._tasks:
            if task.id == task_id:
                logger.debug(f"Tâche trouvée: ID={task_id}")
                return task
        
        logger.warning(f"Tâche non trouvée: ID={task_id}")
        raise TaskNotFoundError(f"Tâche avec l'ID {task_id} non trouvée")

app = FastAPI()

@app.get("/tasks/{task_id}")
def get_task(task_id: int) -> Task:
    """Récupère une tâche spécifique."""
    try:
        logger.info(f"Récupération de la tâche: ID={task_id}")
        return task_service.get_by_id(task_id)
    except TaskNotFoundError as e:
        logger.warning(f"Erreur: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
```

## 10. Checklist d'Audit

- [ ] Tous les noms de fonction sont en `snake_case`
- [ ] Toutes les classes sont en `PascalCase`
- [ ] Les exceptions héritent de la classe personnalisée
- [ ] Tous les paramètres et retours ont des type hints
- [ ] Les docstrings sont présentes sur toutes les fonctions publiques
- [ ] Les logs sont structurés avec le bon niveau (INFO, DEBUG, WARNING, ERROR)
- [ ] Les codes HTTP sont corrects pour chaque cas
- [ ] Les tests couvrent les cas nominaux et les erreurs
- [ ] Pas de code mort ou de commentaires obsolètes
- [ ] La documentation est à jour

