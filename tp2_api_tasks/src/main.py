"""
API REST pour gérer les tâches avec FastAPI.
Fournit des endpoints CRUD pour créer, lire, mettre à jour et supprimer des tâches.
"""

import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel, Field
import uvicorn


# ============================================================================
# Configuration des Logs
# ============================================================================

logger = logging.getLogger(__name__)

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# ============================================================================
# Exceptions Personnalisées
# ============================================================================

class TaskNotFoundError(Exception):
    """Exception levée quand une tâche n'est pas trouvée."""
    pass


class TaskValidationError(Exception):
    """Exception levée en cas d'erreur de validation de tâche."""
    pass


# ============================================================================
# Modèles Pydantic
# ============================================================================

class Task(BaseModel):
    """
    Modèle représentant une tâche.
    
    Attributs:
        id (int): Identifiant unique de la tâche.
        title (str): Titre de la tâche.
        done (bool): Statut de complétion. Par défaut, False.
        description (Optional[str]): Description détaillée de la tâche.
    
    Exemple:
        >>> task = Task(id=1, title="Acheter du lait", done=False)
        >>> print(task.title)
        Acheter du lait
    """
    id: int = Field(..., description="Identifiant unique de la tâche")
    title: str = Field(..., min_length=1, max_length=255, description="Titre de la tâche")
    done: bool = Field(default=False, description="Statut de complétion")
    description: Optional[str] = Field(default=None, description="Description optionnelle")


class TaskCreate(BaseModel):
    """Modèle pour la création d'une tâche (sans ID)."""
    title: str = Field(..., min_length=1, max_length=255, description="Titre de la tâche")
    description: Optional[str] = Field(default=None, description="Description optionnelle")


class TaskUpdate(BaseModel):
    """Modèle pour la mise à jour d'une tâche."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    done: Optional[bool] = Field(default=None)


# ============================================================================
# Service de Tâches (Logique Métier)
# ============================================================================

class TaskService:
    """Service de gestion des tâches."""
    
    def __init__(self) -> None:
        """Initialise le service avec une liste vide et un compteur d'ID."""
        self._tasks: List[Task] = []
        self._next_id: int = 1
        logger.info("Service de tâches initialisé")
    
    def create(self, task_create: TaskCreate) -> Task:
        """
        Crée une nouvelle tâche.
        
        Args:
            task_create (TaskCreate): Données de la tâche à créer.
            
        Returns:
            Task: La tâche créée avec un ID généré.
            
        Raises:
            TaskValidationError: Si les données de la tâche sont invalides.
        """
        try:
            task = Task(
                id=self._next_id,
                title=task_create.title,
                description=task_create.description,
                done=False
            )
            self._tasks.append(task)
            self._next_id += 1
            logger.info(f"Tâche créée: ID={task.id}, Titre='{task.title}'")
            return task
        except Exception as e:
            logger.error(f"Erreur lors de la création de tâche: {str(e)}")
            raise TaskValidationError(f"Erreur lors de la création: {str(e)}")
    
    def get_all(self) -> List[Task]:
        """
        Récupère toutes les tâches.
        
        Returns:
            List[Task]: Liste de toutes les tâches.
        """
        logger.debug(f"Récupération de {len(self._tasks)} tâches")
        return self._tasks.copy()
    
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
        for task in self._tasks:
            if task.id == task_id:
                logger.debug(f"Tâche trouvée: ID={task_id}")
                return task
        logger.warning(f"Tâche non trouvée: ID={task_id}")
        raise TaskNotFoundError(f"Tâche avec l'ID {task_id} non trouvée")
    
    def update(self, task_id: int, task_update: TaskUpdate) -> Task:
        """
        Met à jour une tâche existante.
        
        Args:
            task_id (int): L'ID de la tâche à mettre à jour.
            task_update (TaskUpdate): Données à mettre à jour.
            
        Returns:
            Task: La tâche mise à jour.
            
        Raises:
            TaskNotFoundError: Si la tâche n'existe pas.
        """
        task = self.get_by_id(task_id)
        
        updates = []
        if task_update.title is not None:
            task.title = task_update.title
            updates.append(f"title='{task_update.title}'")
        if task_update.description is not None:
            task.description = task_update.description
            updates.append(f"description='{task_update.description}'")
        if task_update.done is not None:
            task.done = task_update.done
            updates.append(f"done={task_update.done}")
        
        if updates:
            logger.info(f"Tâche mise à jour: ID={task_id}, Changements=[{', '.join(updates)}]")
        else:
            logger.debug(f"Aucune modification pour la tâche: ID={task_id}")
        
        return task
    
    def toggle(self, task_id: int) -> Task:
        """
        Bascule l'état de complétion d'une tâche.
        
        Args:
            task_id (int): L'ID de la tâche à basculer.
            
        Returns:
            Task: La tâche avec son nouvel état.
            
        Raises:
            TaskNotFoundError: Si la tâche n'existe pas.
        """
        task = self.get_by_id(task_id)
        task.done = not task.done
        logger.info(f"Tâche basculée: ID={task_id}, Nouvel état={task.done}")
        return task
    
    def delete(self, task_id: int) -> None:
        """
        Supprime une tâche.
        
        Args:
            task_id (int): L'ID de la tâche à supprimer.
            
        Raises:
            TaskNotFoundError: Si la tâche n'existe pas.
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                self._tasks.pop(i)
                logger.info(f"Tâche supprimée: ID={task_id}")
                return
        logger.warning(f"Tentative de suppression de tâche inexistante: ID={task_id}")
        raise TaskNotFoundError(f"Tâche avec l'ID {task_id} non trouvée")


# ============================================================================
# Application FastAPI
# ============================================================================

app = FastAPI(
    title="API Tasks Manager",
    description="API REST pour gérer les tâches",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instance du service
task_service = TaskService()


# ============================================================================
# Endpoints (Routes)
# ============================================================================

@app.get("/", tags=["Info"])
def read_root() -> dict:
    """
    Endpoint racine - Bienvenue et informations sur l'API.
    
    Retourne un message de bienvenue avec une liste de tous les endpoints
    disponibles. Utilisez cet endpoint pour vérifier que l'API est en ligne.
    
    Returns:
        dict: Message de bienvenue et informations sur l'API.
    
    Examples:
        curl: curl http://localhost:8000/
        
        Python:
        import requests
        response = requests.get("http://localhost:8000/")
        print(response.json())
    """
    logger.info("Accès à l'endpoint racine")
    return {
        "message": "Bienvenue sur l'API Task Manager",
        "version": "1.0.0",
        "docs": "/api/docs",
        "endpoints": {
            "GET /tasks": "Récupérer toutes les tâches",
            "POST /tasks": "Créer une nouvelle tâche",
            "GET /tasks/{id}": "Récupérer une tâche spécifique",
            "PATCH /tasks/{id}": "Mettre à jour une tâche",
            "PATCH /tasks/{id}/toggle": "Basculer l'état d'une tâche",
            "DELETE /tasks/{id}": "Supprimer une tâche"
        }
    }


@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
def list_tasks(done: Optional[bool] = None) -> List[Task]:
    """
    Récupère toutes les tâches avec filtrage optionnel.
    
    Retourne une liste de toutes les tâches. Vous pouvez filtrer par statut
    en utilisant le paramètre de requête 'done'.
    
    Query Parameters:
        done (Optional[bool]): Filtrer par statut de complétion (true/false).
                              Si non spécifié, retourne toutes les tâches.
    
    Returns:
        List[Task]: Liste de toutes les tâches (ou filtrées).
    
    Examples:
        Récupérer toutes les tâches:
        curl http://localhost:8000/tasks
        
        Récupérer uniquement les tâches complétées:
        curl http://localhost:8000/tasks?done=true
        
        Récupérer uniquement les tâches en cours:
        curl http://localhost:8000/tasks?done=false
        
        Python:
        import requests
        response = requests.get("http://localhost:8000/tasks")
        tasks = response.json()
    """
    logger.info(f"Listage des tâches (filtre done={done})")
    tasks = task_service.get_all()
    
    if done is not None:
        tasks = [task for task in tasks if task.done == done]
        logger.info(f"Filtre appliqué: {len(tasks)} tâches avec done={done}")
    
    return tasks


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task_create: TaskCreate) -> Task:
    """
    Crée une nouvelle tâche.
    
    Crée une nouvelle tâche et la retourne avec un ID généré automatiquement.
    Le statut de complétion est défini à false par défaut.
    
    Request Body:
        - title (str): Titre de la tâche (requis, 1-255 caractères).
        - description (str, optional): Description détaillée de la tâche.
    
    Returns:
        Task: La tâche créée avec son ID généré.
    
    Examples:
        curl: curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Acheter du lait","description":"Lait entier, 1L"}'
        
        Python:
        import requests
        response = requests.post(
            "http://localhost:8000/tasks",
            json={"title": "Acheter du lait", "description": "Lait entier, 1L"}
        )
        new_task = response.json()
    """
    try:
        logger.info(f"Création de tâche: title='{task_create.title}'")
        return task_service.create(task_create)
    except TaskValidationError as e:
        logger.error(f"Erreur de validation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def get_task(task_id: int) -> Task:
    """
    Récupère une tâche spécifique par son ID.
    
    Retourne les détails complets d'une tâche identifiée par son ID.
    
    Path Parameters:
        task_id (int): L'ID unique de la tâche à récupérer.
    
    Returns:
        Task: La tâche demandée.
    
    Raises:
        HTTPException 404: Si la tâche n'existe pas.
    
    Examples:
        curl: curl http://localhost:8000/tasks/1
        
        Python:
        import requests
        response = requests.get("http://localhost:8000/tasks/1")
        if response.status_code == 200:
            task = response.json()
    """
    try:
        logger.info(f"Récupération de la tâche: ID={task_id}")
        return task_service.get_by_id(task_id)
    except TaskNotFoundError as e:
        logger.warning(f"Tâche non trouvée: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@app.patch("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def update_task(task_id: int, task_update: TaskUpdate) -> Task:
    """
    Met à jour une tâche existante (mise à jour partielle).
    
    Permet de modifier un ou plusieurs champs d'une tâche.
    Les champs non spécifiés ne sont pas modifiés.
    
    Path Parameters:
        task_id (int): L'ID de la tâche à mettre à jour.
    
    Request Body (tous les champs optionnels):
        - title (str): Nouveau titre (optionnel).
        - description (str): Nouvelle description (optionnel).
        - done (bool): Nouveau statut (optionnel).
    
    Returns:
        Task: La tâche mise à jour.
    
    Raises:
        HTTPException 404: Si la tâche n'existe pas.
    
    Examples:
        Mettre à jour le titre et le statut:
        curl -X PATCH http://localhost:8000/tasks/1 -H "Content-Type: application/json" -d '{"title":"Acheter du lait 2L","done":true}'
        
        Python:
        import requests
        response = requests.patch(
            "http://localhost:8000/tasks/1",
            json={"title": "Acheter du lait 2L", "done": True}
        )
    """
    try:
        logger.info(f"Mise à jour de la tâche: ID={task_id}")
        return task_service.update(task_id, task_update)
    except TaskNotFoundError as e:
        logger.warning(f"Tâche non trouvée: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@app.patch("/tasks/{task_id}/toggle", response_model=Task, tags=["Tasks"])
def toggle_task(task_id: int) -> Task:
    """
    Bascule l'état de complétion d'une tâche.
    
    Inverse le statut de complétion: true devient false, false devient true.
    Utile pour marquer une tâche comme complétée ou non-complétée rapidement.
    
    Path Parameters:
        task_id (int): L'ID de la tâche à basculer.
    
    Returns:
        Task: La tâche avec son nouvel état.
    
    Raises:
        HTTPException 404: Si la tâche n'existe pas.
    
    Examples:
        curl: curl -X PATCH http://localhost:8000/tasks/1/toggle
        
        Python:
        import requests
        response = requests.patch("http://localhost:8000/tasks/1/toggle")
        task = response.json()
    """
    try:
        logger.info(f"Basculement de la tâche: ID={task_id}")
        return task_service.toggle(task_id)
    except TaskNotFoundError as e:
        logger.warning(f"Tâche non trouvée: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(task_id: int) -> None:
    """
    Supprime une tâche de manière permanente.
    
    La tâche est supprimée de la base de données. Cette action ne peut pas
    être annulée. La réponse est vide (204 No Content).
    
    Path Parameters:
        task_id (int): L'ID de la tâche à supprimer.
    
    Returns:
        None: Pas de contenu (code 204 No Content).
    
    Raises:
        HTTPException 404: Si la tâche n'existe pas.
    
    Examples:
        curl: curl -X DELETE http://localhost:8000/tasks/1
        
        Python:
        import requests
        response = requests.delete("http://localhost:8000/tasks/1")
        if response.status_code == 204:
            print("Tache supprimee avec succes")
    """
    try:
        logger.info(f"Suppression de la tâche: ID={task_id}")
        task_service.delete(task_id)
    except TaskNotFoundError as e:
        logger.warning(f"Tâche non trouvée: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@app.get("/stats", tags=["Stats"])
def get_statistics() -> dict:
    """
    Récupère les statistiques sur l'ensemble des tâches.
    
    Retourne des statistiques utiles sur vos tâches: nombre total, nombre
    de tâches complétées, nombre en cours, et pourcentage de completion.
    
    Returns:
        dict: Statistiques incluant le total, en cours, terminées, et pourcentage.
    
    Examples:
        curl: curl http://localhost:8000/stats
        
        Python:
        import requests
        response = requests.get("http://localhost:8000/stats")
        stats = response.json()
    """
    logger.info("Récupération des statistiques")
    tasks = task_service.get_all()
    total = len(tasks)
    done_count = sum(1 for task in tasks if task.done)
    pending_count = total - done_count
    completion_percentage = round((done_count / total * 100) if total > 0 else 0, 2)
    
    stats = {
        "total": total,
        "en_cours": pending_count,
        "terminees": done_count,
        "pourcentage_completion": completion_percentage
    }
    
    logger.info(f"Statistiques: total={total}, terminees={done_count}, en_cours={pending_count}, completion={completion_percentage}%")
    return stats


# ============================================================================
# Point d'Entrée
# ============================================================================

if __name__ == "__main__":
    logger.info("Démarrage de l'API Task Manager")
    logger.info("Documentation disponible à: http://localhost:8000/api/docs")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
