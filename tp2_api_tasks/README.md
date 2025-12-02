# API Task Manager - README

## 📦 Structure du Projet

```
tp2_api_tasks/
├── src/
│   └── main.py              # Application FastAPI principale
├── tests/
│   └── test_main.py         # Tests unitaires et d'intégration
├── docs/
│   └── API.md               # Documentation complète de l'API
├── requirements.txt         # Dépendances Python
├── pytest.ini              # Configuration pytest
└── README.md               # Ce fichier
```

## 🎯 Objectif

Créer une API REST moderne pour gérer une liste de tâches (TODO list) avec:
- ✅ Endpoints CRUD complets
- ✅ Modèles de données avec Pydantic
- ✅ Documentation automatique Swagger/OpenAPI
- ✅ Tests unitaires complets
- ✅ Gestion d'erreurs robuste
- ✅ Filtrage et statistiques

## ✨ Caractéristiques

### Endpoints Implémentés

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Informations sur l'API |
| GET | `/tasks` | Lister toutes les tâches |
| POST | `/tasks` | Créer une nouvelle tâche |
| GET | `/tasks/{id}` | Récupérer une tâche |
| PATCH | `/tasks/{id}` | Mettre à jour une tâche |
| PATCH | `/tasks/{id}/toggle` | Basculer l'état |
| DELETE | `/tasks/{id}` | Supprimer une tâche |
| GET | `/stats` | Statistiques |

### Modèles Pydantic

```python
# Modèle Task
class Task(BaseModel):
    id: int
    title: str                    # 1-255 caractères
    done: bool = False
    description: Optional[str] = None

# Modèle pour la création
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

# Modèle pour la mise à jour
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None
```

## 🚀 Démarrage Rapide

### 1. Installation
```bash
# Cloner ou accéder au projet
cd tp2_api_tasks

# Créer un environnement virtuel
python -m venv venv
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Lancer l'API
```bash
cd src
python main.py
```

### 3. Accéder à l'API
- **API:** http://localhost:8000
- **Documentation:** http://localhost:8000/api/docs
- **Alternative:** http://localhost:8000/api/redoc

## 🧪 Tests

### Lancer tous les tests
```bash
pytest tests/
```

### Lancer avec verbosité
```bash
pytest tests/test_main.py -v
```

### Voir la couverture de code
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

## 📚 Exemples d'Utilisation

### Créer une tâche
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Acheter du lait","description":"1L"}'
```

### Lister les tâches
```bash
curl http://localhost:8000/tasks
```

### Filtrer les tâches terminées
```bash
curl http://localhost:8000/tasks?done=true
```

### Basculer une tâche
```bash
curl -X PATCH http://localhost:8000/tasks/1/toggle
```

### Supprimer une tâche
```bash
curl -X DELETE http://localhost:8000/tasks/1
```

## 🏗️ Architecture

### Couches

1. **Models** (main.py)
   - Task, TaskCreate, TaskUpdate (Pydantic)

2. **Service** (TaskService)
   - Logique métier
   - Gestion des tâches

3. **API** (Endpoints FastAPI)
   - Routes HTTP
   - Gestion des erreurs
   - Réponses JSON

### Flux de Requête

```
Client HTTP
    ↓
Route FastAPI (validation Pydantic)
    ↓
TaskService (logique métier)
    ↓
Response JSON
    ↓
Client HTTP
```

## ⚙️ Configuration

### Serveur (src/main.py)
```python
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
```

### Changements possibles
- `host="0.0.0.0"` pour accès externe
- `port=3000` pour un autre port
- `reload=False` pour la production
- `log_level="debug"` pour plus de logs

## 🔐 Sécurité

Actuellement:
- ⚠️ Pas d'authentification
- ⚠️ CORS ouvert à tous (`allow_origins=["*"]`)
- ⚠️ Données stockées en mémoire (non persistantes)

Pour la production:
- [ ] Ajouter JWT/OAuth2
- [ ] Configurer CORS correctement
- [ ] Ajouter une base de données
- [ ] Implémenter le rate limiting
- [ ] Valider les entrées côté serveur

## 📊 Statistiques API

Le endpoint `/stats` retourne:
```json
{
  "total": 10,
  "en_cours": 7,
  "terminees": 3,
  "pourcentage_completion": 30.0
}
```

## 🐛 Dépannage

### Port déjà utilisé
```bash
# Changer le port
uvicorn main:app --port 8001
```

### Erreur de dépendances
```bash
# Réinstaller
pip install --upgrade -r requirements.txt
```

### Tests ne trouvent pas le module
```bash
# Depuis le dossier projet
python -m pytest tests/
```

## 📖 Documentation Complète

Voir `docs/API.md` pour:
- Endpoint détaillés
- Exemples de requêtes
- Codes de statut HTTP
- Modèles de données complets
- Guides de déploiement

## 🎓 Concept de Copilot

Ce projet démontre comment utiliser GitHub Copilot pour:

1. **Générer la structure** - Créer dossiers et fichiers
2. **Implémenter les modèles** - Pydantic avec validation
3. **Créer les endpoints** - FastAPI avec documentation auto
4. **Écrire les tests** - Pytest complet
5. **Générer la documentation** - Docstrings et README

### Bons Prompts Copilot

```
"Crée une API REST FastAPI avec modèles Pydantic pour gérer des tâches.
Implémente les opérations CRUD avec endpoints:
GET /tasks, POST /tasks, GET /tasks/{id}, PATCH /tasks/{id}, DELETE /tasks/{id}
Ajoute la validation Pydantic et la gestion d'erreurs."
```

## 🚀 Améliorations Futures

1. **Persistance**
   - Intégrer SQLAlchemy
   - Ajouter PostgreSQL/MongoDB

2. **Authentification**
   - Implémenter JWT
   - Ajouter OAuth2

3. **Fonctionnalités**
   - Ajouter les priorités
   - Ajouter les catégories
   - Ajouter les dates d'échéance
   - Implémenter les rappels

4. **Performance**
   - Ajouter la pagination
   - Implémenter le caching
   - Ajouter l'indexation BD

5. **Déploiement**
   - Docker
   - CI/CD (GitHub Actions)
   - Déployer sur Heroku/AWS/DigitalOcean

## 📝 Licence

Exercice pédagogique - Formation IA avec GitHub Copilot

## 🤝 Contribution

Suggestions de fonctionnalités:
- Ajouter les sous-tâches
- Implémenter les étiquettes
- Ajouter la collaboration
- Support multi-utilisateurs

---

**Bon développement avec FastAPI et Copilot! 🚀**
