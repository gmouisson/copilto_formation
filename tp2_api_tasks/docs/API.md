# API Task Manager

## 📋 Description

API REST pour gérer des tâches (TODO list). Construit avec **FastAPI** et **Pydantic** pour un typage complet et une documentation automatique.

## 🎯 Fonctionnalités

- ✅ Créer des tâches
- ✅ Lister toutes les tâches (avec filtrage)
- ✅ Récupérer une tâche spécifique
- ✅ Mettre à jour une tâche
- ✅ Basculer l'état d'une tâche
- ✅ Supprimer une tâche
- ✅ Voir les statistiques

## 🛠️ Stack Technologique

| Composant | Technologie |
|-----------|------------|
| **Framework Web** | FastAPI |
| **Serveur** | Uvicorn |
| **Validation** | Pydantic |
| **Tests** | Pytest |
| **Documentation** | Swagger (automatique) |
| **Langage** | Python 3.8+ |

## 📦 Installation

### 1. Cloner le projet
```bash
cd tp2_api_tasks
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

## 🚀 Démarrage

### Lancer l'API
```bash
cd src
python main.py
```

L'API sera accessible à: **http://localhost:8000**

Documentation interactive: **http://localhost:8000/api/docs**

## 📚 Endpoints

### Informations

```http
GET /
```
Récupère les informations sur l'API.

### Tâches

#### Lister toutes les tâches
```http
GET /tasks
GET /tasks?done=true
GET /tasks?done=false
```

**Réponse (200):**
```json
[
  {
    "id": 1,
    "title": "Acheter du lait",
    "done": false,
    "description": null
  }
]
```

#### Créer une tâche
```http
POST /tasks
Content-Type: application/json

{
  "title": "Acheter du lait",
  "description": "Lait entier, 1L"
}
```

**Réponse (201):**
```json
{
  "id": 1,
  "title": "Acheter du lait",
  "done": false,
  "description": "Lait entier, 1L"
}
```

#### Récupérer une tâche
```http
GET /tasks/1
```

**Réponse (200):**
```json
{
  "id": 1,
  "title": "Acheter du lait",
  "done": false,
  "description": "Lait entier, 1L"
}
```

#### Mettre à jour une tâche
```http
PATCH /tasks/1
Content-Type: application/json

{
  "title": "Acheter du lait 2L",
  "done": true
}
```

**Réponse (200):**
```json
{
  "id": 1,
  "title": "Acheter du lait 2L",
  "done": true,
  "description": "Lait entier, 1L"
}
```

#### Basculer l'état d'une tâche
```http
PATCH /tasks/1/toggle
```

**Réponse (200):**
```json
{
  "id": 1,
  "title": "Acheter du lait",
  "done": true,
  "description": null
}
```

#### Supprimer une tâche
```http
DELETE /tasks/1
```

**Réponse (204):** Pas de contenu

### Statistiques

```http
GET /stats
```

**Réponse (200):**
```json
{
  "total": 10,
  "en_cours": 7,
  "terminees": 3,
  "pourcentage_completion": 30.0
}
```

## 🧪 Tests

### Lancer les tests
```bash
cd tests
pytest test_main.py -v
```

### Couverture de tests
```bash
pytest test_main.py --cov=src --cov-report=html
```

## 📋 Modèle de Données

### Task
```python
class Task(BaseModel):
    id: int              # Identifiant unique
    title: str           # Titre (1-255 caractères)
    done: bool          # Statut de complétion
    description: str    # Description optionnelle
```

### TaskCreate
```python
class TaskCreate(BaseModel):
    title: str              # Titre (requis)
    description: str        # Description (optionnelle)
```

### TaskUpdate
```python
class TaskUpdate(BaseModel):
    title: str             # Nouveau titre (optionnel)
    description: str       # Nouvelle description (optionnelle)
    done: bool            # Nouveau statut (optionnel)
```

## 🔍 Codes de Statut HTTP

| Code | Signification |
|------|--------------|
| **200** | Succès (GET, PATCH) |
| **201** | Créé (POST) |
| **204** | Pas de contenu (DELETE) |
| **404** | Non trouvé |
| **422** | Erreur de validation |

## 💡 Exemples d'Utilisation

### Avec curl

```bash
# Créer une tâche
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Ma première tâche"}'

# Lister les tâches
curl http://localhost:8000/tasks

# Basculer une tâche
curl -X PATCH http://localhost:8000/tasks/1/toggle

# Supprimer une tâche
curl -X DELETE http://localhost:8000/tasks/1
```

### Avec Python requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Créer une tâche
response = requests.post(
    f"{BASE_URL}/tasks",
    json={"title": "Ma tâche"}
)
print(response.json())

# Lister les tâches
response = requests.get(f"{BASE_URL}/tasks")
print(response.json())

# Basculer une tâche
response = requests.patch(f"{BASE_URL}/tasks/1/toggle")
print(response.json())
```

## 📖 Documentation API Interactive

Accédez à la documentation interactive Swagger:
- **URL:** http://localhost:8000/api/docs
- Testez directement les endpoints
- Voyez les schémas Pydantic
- Essayez les requêtes

## 🔧 Configuration

### Paramètres du serveur
Dans `src/main.py`:
```python
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",      # Changer pour "0.0.0.0" pour accès externe
        port=8000,              # Port personnalisé
        reload=True,            # Hot-reload (désactiver en prod)
        log_level="info"
    )
```

## 📝 Notes de Développement

- Les tâches sont stockées en mémoire (réinitialisation à chaque démarrage)
- Pour la persistance, intégrez une base de données (SQLAlchemy, MongoDB, etc.)
- Ajoutez l'authentification pour la sécurisation
- Implémentez les dates (created_at, updated_at)
- Ajoutez les priorités et catégories

## 🚀 Prochaines Étapes

- [ ] Ajouter une base de données (PostgreSQL, MongoDB)
- [ ] Implémentation l'authentification JWT
- [ ] Ajouter les timestamps (created_at, updated_at)
- [ ] Implémenter les priorités
- [ ] Ajouter le système de catégories
- [ ] Limiter l'accès par utilisateur
- [ ] Déployer sur AWS/Heroku/DigitalOcean
- [ ] Ajouter des logs structurés
- [ ] Implémenter le rate limiting

## 📄 Licence

Ce projet est un exercice pédagogique pour la Formation IA avec GitHub Copilot.
