# 📋 Gestionnaire de Tâches CLI

Un gestionnaire de tâches simple et efficace en ligne de commande, développé avec Python. Ce projet démontre les bonnes pratiques de développement avec GitHub Copilot.

---

## 🚀 Installation

### Prérequis
- **Python 3.7+** installé sur votre système
- Accès à un terminal/invite de commande

### Étapes d'installation

1. **Clonez ou téléchargez le projet**
   ```bash
   cd tp2_task_manager
   ```

2. **Vérifiez que Python est installé**
   ```bash
   python --version
   ```

3. **Aucune dépendance externe requise** ✅
   Le projet utilise uniquement les bibliothèques standard Python (`argparse`, `json`, `os`)

---

## 📖 Guide d'Utilisation

### Commandes Disponibles

#### 1. **Ajouter une tâche**
```bash
python cli.py add "Titre de votre tâche"
```

**Exemple:**
```bash
python cli.py add "Acheter du lait"
python cli.py add "Terminer le rapport"
```

**Résultat:**
```
Tâche ajoutée: [1] Acheter du lait - NOT DONE
```

---

#### 2. **Lister toutes les tâches**
```bash
python cli.py list
```

**Résultat:**
```
[1] Acheter du lait - NOT DONE
[2] Terminer le rapport - NOT DONE
[3] Appeler le client - DONE
```

---

#### 3. **Marquer une tâche comme terminée/non-terminée**
```bash
python cli.py toggle <ID>
```

**Exemple:**
```bash
python cli.py toggle 1
```

**Résultat:**
```
Tâche mise à jour: [1] Acheter du lait - DONE
```

> 💡 **Conseil:** La commande `toggle` bascule l'état. Exécutez-la à nouveau pour marquer comme non-terminée.

---

#### 4. **Supprimer une tâche**
```bash
python cli.py delete <ID>
```

**Exemple:**
```bash
python cli.py delete 2
```

**Résultat:**
```
Tâche avec ID 2 supprimée.
```

---

## 💾 Stockage des Données

- Les tâches sont sauvegardées automatiquement dans un fichier `tasks.json`
- Les données persistent entre les sessions
- Aucune configuration supplémentaire nécessaire

**Structure du fichier `tasks.json`:**
```json
[
    {
        "id": 1,
        "title": "Acheter du lait",
        "done": true
    },
    {
        "id": 2,
        "title": "Terminer le rapport",
        "done": false
    }
]
```

---

## 🔧 Architecture du Projet

### Fichiers Principaux

| Fichier | Description |
|---------|-------------|
| `app.py` | Définition des classes `Task` et `TaskService` |
| `cli.py` | Interface en ligne de commande avec argparse |
| `storage.py` | Gestion du stockage JSON et classes de données |

### Hiérarchie des Composants

```
TaskService (Gestion métier)
    ├── ajouter_tache()      - Crée une nouvelle tâche
    ├── lister_taches()      - Récupère toutes les tâches
    ├── etat_tache()         - Bascule l'état d'une tâche
    └── supprimer_tache()    - Supprime une tâche

Storage (Persistance)
    ├── load_tasks()         - Charge les tâches depuis JSON
    └── save_tasks()         - Sauvegarde les tâches en JSON
```

---

## 📚 Exemples Pratiques

### Exemple 1: Créer une liste de courses
```bash
python cli.py add "Lait"
python cli.py add "Pain"
python cli.py add "Œufs"
python cli.py add "Fromage"
python cli.py list
```

### Exemple 2: Gérer des tâches quotidiennes
```bash
# Ajouter les tâches de la journée
python cli.py add "Vérifier les emails"
python cli.py add "Réunion d'équipe à 10h"
python cli.py add "Répondre aux tickets support"

# Lister pour voir tout
python cli.py list

# Marquer comme terminée
python cli.py toggle 1

# Voir la mise à jour
python cli.py list
```

### Exemple 3: Nettoyer la liste
```bash
# Supprimer les tâches obsolètes
python cli.py delete 2
python cli.py delete 3

# Vérifier le résultat
python cli.py list
```

---

## 🤖 Bonnes Pratiques avec GitHub Copilot

### 1. **Prompts Clairs et Spécifiques**

❌ **Mauvais prompt:**
```
Crée une fonction
```

✅ **Bon prompt:**
```
Crée une fonction Python qui ajoute une tâche avec un titre et retourne 
la tâche créée avec un identifiant unique auto-incrémenté.
```

---

### 2. **Contexte Structuré**

❌ **Mauvais:**
```
Ajoute un truc pour gérer les tâches
```

✅ **Bon:**
```
Ajoute une méthode 'basculer_etat_tache(id: int)' à la classe TaskService 
qui inverse le statut 'done' d'une tâche et retourne la tâche modifiée.
Lève une ValueError si la tâche n'existe pas.
```

---

### 3. **Spécifier le Format de Sortie**

❌ **Imprécis:**
```
Fais une fonction qui affiche les tâches
```

✅ **Précis:**
```
Crée une fonction qui affiche chaque tâche avec le format:
[ID] Titre - DONE ou NOT DONE
Où DONE s'affiche si la tâche est complétée, sinon NOT DONE.
```

---

### 4. **Demander des Commentaires et Docstrings**

✅ **Bon prompt:**
```
Implémente la méthode supprimer_tache(id: int) -> bool avec:
- Une docstring expliquant que ça supprime une tâche
- Des commentaires sur la logique
- Le type de retour: True si succès, False si tâche non trouvée
```

---

### 5. **Progresser Étape par Étape**

✅ **Structure recommandée:**

**Étape 1:** Créer la structure de classe
```
Crée une classe Task avec id (int), title (str), et done (bool = False)
```

**Étape 2:** Implémenter la logique CRUD
```
Crée une classe TaskService avec la méthode ajouter_tache(title: str) -> Task
```

**Étape 3:** Ajouter la persistance
```
Crée une fonction load_tasks() qui charge les tâches depuis un JSON
```

**Étape 4:** Construire l'interface CLI
```
Crée une interface CLI avec argparse pour les commandes: add, list, toggle, delete
```

---

### 6. **Exemples et Cas d'Usage**

✅ **Excellent prompt:**
```
Crée une méthode qui filtre les tâches non terminées. 
Retourne une liste de Task.
Exemple d'usage:
    service = TaskService()
    service.ajouter_tache("Task 1")
    service.etat_tache(1)  # Marque comme terminée
    service.ajouter_tache("Task 2")
    taches_en_cours = service.lister_taches_en_cours()
    # taches_en_cours contient uniquement Task 2
```

---

### 7. **Demander les Tests et Validation**

✅ **Complet:**
```
Crée une fonction validate_task(task: Task) -> bool qui vérifie:
- Le titre n'est pas vide
- L'id est positif
Retourne True si valide, False sinon.
Ajoute des commentaires et des exemples d'usage.
```

---

## 🎯 Conseils d'Utilisation Avancés

### Intégration avec Copilot

1. **Utilisez des commentaires comme prompts**
   ```python
   # TODO: Ajouter une méthode pour exporter les tâches en CSV
   # Cette méthode doit lire toutes les tâches et les exporter avec le format:
   # id, titre, statut
   ```

2. **Demandez des refactorisations**
   ```
   Refactorise le code CLI pour améliorer la lisibilité et 
   séparer la logique de présentation de la logique métier.
   ```

3. **Demandez des tests unitaires**
   ```
   Crée des tests unitaires pour la classe TaskService 
   en utilisant le module unittest de Python.
   ```

---

## ❓ Dépannage

### Erreur: "Tâche non trouvée"
**Solution:** Vérifiez que l'ID de la tâche existe avec `python cli.py list`

### Erreur: "tasks.json non trouvé"
**Solution:** Ajoutez votre première tâche: `python cli.py add "Ma première tâche"`

### Erreur: "invalid choice: 'commande'"
**Solution:** Utilisez une commande valide: `add`, `list`, `toggle`, ou `delete`

---

## 📝 Résumé des Commandes

```bash
# Ajouter
python cli.py add "Nouvelle tâche"

# Lister
python cli.py list

# Basculer l'état
python cli.py toggle 1

# Supprimer
python cli.py delete 1

# Aide
python cli.py --help
```

---

## 🎓 Apprentissage avec Copilot

Ce projet est un excellent exemple pour apprendre à:
- ✅ Écrire des prompts efficaces pour Copilot
- ✅ Structurer une application Python
- ✅ Implémenter des opérations CRUD
- ✅ Gérer la persistance de données
- ✅ Créer une interface CLI professionnelle

**Exercice suggéré:** Utilisez Copilot pour ajouter les fonctionnalités suivantes:
- [ ] Filtrer les tâches par état (terminées/non-terminées)
- [ ] Ajouter une date limite (due_date) aux tâches
- [ ] Exporter les tâches en CSV/JSON
- [ ] Rechercher les tâches par mot-clé
- [ ] Trier les tâches par ID ou titre

---

## 📄 Licence

Ce projet est un exercice pédagogique pour la Formation IA avec GitHub Copilot.

---

## 🤝 Contribution

Améliorations suggérées avec Copilot:
1. Ajouter des tests unitaires
2. Implémenter la validation des entrées
3. Ajouter un système de catégories
4. Créer une interface graphique (GUI)

---

**Bonne utilisation et bon apprentissage avec GitHub Copilot! 🚀**
