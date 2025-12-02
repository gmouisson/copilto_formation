# Calculatrice CLI - Documentation

Une calculatrice en ligne de commande avec historique des opérations, mode interactif et tests complets.

## 📋 Table des matières

- [Installation](#installation)
- [Exécution](#exécution)
- [Structure du projet](#structure-du-projet)
- [Utilisation](#utilisation)
- [Tests](#tests)
- [Fonctionnalités](#fonctionnalités)

---

## 🔧 Installation

### Prérequis

- **Python 3.7+** (testé avec Python 3.12.1)
- **pip** (gestionnaire de paquets Python)

### Étapes d'installation

#### 1. Cloner ou télécharger le projet
```bash
cd C:\guillaume\Formations\Formation_IA_Copilot\tp_calc_cli
```

#### 2. Créer un environnement virtuel (recommandé)
```bash
python -m venv .venv
```

#### 3. Activer l'environnement virtuel

**Sur Windows (PowerShell) :**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Sur Windows (CMD) :**
```cmd
.venv\Scripts\activate.bat
```

**Sur macOS/Linux :**
```bash
source .venv/bin/activate
```

#### 4. Installer les dépendances

```bash
pip install pytest
```

---

## 🚀 Exécution

### Mode interactif (recommandé pour l'exploration)

Lancer la calculatrice en mode interactif :

```bash
python calc_cli.py interactive
```

ou simplement :

```bash
python calc_cli.py
```

**Commandes disponibles en mode interactif :**

| Commande | Description | Exemple |
|----------|-------------|---------|
| `add a b` | Addition | `add 5 3` |
| `sub a b` | Soustraction | `sub 10 4` |
| `mul a b` | Multiplication | `mul 4 5` |
| `div a b` | Division | `div 20 4` |
| `history` | Affiche l'historique | `history` |
| `stats` | Affiche les statistiques | `stats` |
| `clear` | Efface l'historique | `clear` |
| `quit` | Quitter le programme | `quit` |

**Exemple d'utilisation :**

```
>>> add 5 3
✓ Résultat: 5.0 + 3.0 = 8.0000

>>> history
======================================================================
HISTORIQUE DES OPÉRATIONS
======================================================================

1. [2025-12-01T14:30:45.123456]
   Opération: 5.0 + 3.0 = 8.0000

>>> quit
Au revoir!
```

### Mode ligne de commande

Exécuter une seule opération directement :

```bash
# Addition
python calc_cli.py add 5 3

# Soustraction
python calc_cli.py sub 10 4

# Multiplication
python calc_cli.py mul 4 5

# Division
python calc_cli.py div 20 4
```

**Résultats :**
```
5.0 + 3.0 = 8.0000
10.0 - 4.0 = 6.0000
4.0 * 5.0 = 20.0000
20.0 / 4.0 = 5.0000
```

---

## 📁 Structure du projet

```
tp_calc_cli/
├── calc.py              # Fonctions mathématiques de base (add, sub, mul, div)
├── calc_cli.py          # Interface CLI avec argparse
├── calc_storage.py      # Gestion de l'historique JSON
├── test_calc.py         # Suite de tests complète (pytest)
├── calc_history.json    # Historique des opérations (créé automatiquement)
├── README.md            # Ce fichier
└── .venv/               # Environnement virtuel Python
```

### Description des fichiers

#### **calc.py**
Contient les 4 fonctions mathématiques :
- `add(a, b)` : Retourne a + b
- `sub(a, b)` : Retourne a - b
- `mul(a, b)` : Retourne a * b
- `div(a, b)` : Retourne a / b (lève ValueError si b = 0)

Chaque fonction possède une docstring détaillée avec exemples.

#### **calc_cli.py**
Interface en ligne de commande avec :
- **Mode interactif** : Boucle interactive pour múltiples opérations
- **Mode CLI** : Exécution d'une seule opération
- Utilise `argparse` pour le parsing des arguments
- Intégration avec `calc_storage.py` pour la sauvegarde

#### **calc_storage.py**
Gestion persistante des données :
- `save_operation()` : Sauvegarde une opération en JSON
- `load_history()` : Charge l'historique
- `display_history()` : Affiche formaté
- `clear_history()` : Efface l'historique
- `get_history_stats()` : Retourne les statistiques

#### **test_calc.py**
Suite de tests pytest complète avec :
- **40+ tests** organisés par catégorie
- Tests de cas simples, négatifs, décimaux
- Tests d'erreur (division par zéro)
- Tests paramétrés
- Tests d'intégration
- Commentaires détaillés

#### **calc_history.json**
Fichier JSON créé automatiquement contenant :
```json
[
  {
    "timestamp": "2025-12-01T14:30:45.123456",
    "operation": "add",
    "operand_a": 5,
    "operand_b": 3,
    "result": 8
  }
]
```

---

## 💻 Utilisation

### Exemple complet

```bash
# 1. Activer l'environnement (si nécessaire)
.\.venv\Scripts\Activate.ps1

# 2. Lancer le mode interactif
python calc_cli.py

# 3. Dans le mode interactif
>>> add 10 5
✓ Résultat: 10.0 + 5.0 = 15.0000

>>> sub 20 8
✓ Résultat: 20.0 - 8.0 = 12.0000

>>> mul 3.5 2
✓ Résultat: 3.5 * 2.0 = 7.0000

>>> div 100 4
✓ Résultat: 100.0 / 4.0 = 25.0000

>>> history
# Affiche toutes les opérations avec timestamps

>>> stats
📊 STATISTIQUES
Total d'opérations: 4
Additions: 1
Soustractions: 1
Multiplications: 1
Divisions: 1

>>> quit
Au revoir!
```

### Gestion des erreurs

**Division par zéro :**
```bash
>>> div 5 0
❌ Erreur: Erreur : Division par zéro impossible

>>> div 10 0
❌ Erreur: Erreur : Division par zéro impossible
```

**Entrée invalide :**
```bash
>>> add abc 3
❌ Erreur: 'abc' ou '3' n'est pas un nombre valide
   Utilisez des nombres entiers ou décimaux (ex: 5, 3.14)

>>> multiply 5 3
❌ Erreur: Commande 'multiply' inconnue
   Commandes valides: add, sub, mul, div, history, stats, clear
```

---

## 🧪 Tests

### Exécuter tous les tests

```bash
python -m pytest test_calc.py -v
```

### Exécuter un test spécifique

```bash
python -m pytest test_calc.py::TestAdd::test_add_positifs -v
```

### Voir la couverture des tests

```bash
python -m pytest test_calc.py --cov=calc
```

### Résultats attendus

```
test_calc.py::TestAdd::test_add_positifs PASSED           [ 5%]
test_calc.py::TestAdd::test_add_negatifs PASSED           [10%]
test_calc.py::TestAdd::test_add_decimaux PASSED           [15%]
...
test_calc.py::TestParametrises::test_div_parametrise_par_zero PASSED [95%]
============================= 40 passed in 0.52s ==============================
```

### Catégories de tests

- **TestAdd** : 5 tests pour l'addition
- **TestSub** : 5 tests pour la soustraction
- **TestMul** : 6 tests pour la multiplication
- **TestDiv** : 6 tests pour la division
- **TestIntegration** : 3 tests d'intégration
- **TestParametrises** : Tests paramétrés (plusieurs cas par fonction)

---

## 🎯 Fonctionnalités

### Opérations mathématiques
✓ Addition, soustraction, multiplication, division
✓ Support des nombres entiers et décimaux
✓ Support des nombres négatifs
✓ Gestion de la division par zéro

### Interface utilisateur
✓ Mode CLI pour une seule opération
✓ Mode interactif pour múltiples opérations
✓ Messages d'erreur clairs et informatifs
✓ Affichage des résultats avec 4 décimales

### Historique
✓ Sauvegarde automatique en JSON
✓ Affichage de l'historique avec timestamps
✓ Statistiques par opération
✓ Effacement de l'historique

### Qualité du code
✓ Tests pytest complets (40+ tests)
✓ Gestion des erreurs robuste
✓ Docstrings détaillées
✓ Code commenté et structuré

---

## 📊 Format des résultats

Les résultats sont affichés avec **4 décimales** :

```bash
>>> add 1 2
✓ Résultat: 1.0 + 2.0 = 3.0000

>>> div 7 2
✓ Résultat: 7.0 / 2.0 = 3.5000

>>> mul 2.5 4
✓ Résultat: 2.5 * 4.0 = 10.0000
```

---

## 🐛 Dépannage

### "pytest : Le terme n'est pas reconnu"

**Solution :** Installer pytest
```bash
pip install pytest
```

### "ModuleNotFoundError: No module named 'calc'"

**Solution :** Assurez-vous d'être dans le répertoire du projet
```bash
cd C:\guillaume\Formations\Formation_IA_Copilot\tp_calc_cli
python calc_cli.py
```

### L'historique ne se sauvegarde pas

**Vérifier :** Les permissions d'écriture dans le répertoire du projet
```bash
# Vérifier que calc_history.json existe
dir calc_history.json
```

---

## 📝 Exemples supplémentaires

### Calculs complexes

```bash
# Mode CLI
python calc_cli.py add 3.14 2.86      # = 6.0000
python calc_cli.py mul 10.5 2         # = 21.0000
python calc_cli.py div 22 7           # = 3.1429

# Mode interactif
>>> add -5 10
✓ Résultat: -5.0 + 10.0 = 5.0000

>>> sub 0 100
✓ Résultat: 0.0 - 100.0 = -100.0000

>>> mul -2 -3
✓ Résultat: -2.0 * -3.0 = 6.0000
```

---

## 📚 Références

- **argparse** : https://docs.python.org/fr/3/library/argparse.html
- **json** : https://docs.python.org/fr/3/library/json.html
- **pytest** : https://docs.pytest.org/

---

## 👤 Auteur

Formation IA Copilot - TP Calculatrice CLI

---

## 🤖 Bonnes pratiques pour utiliser GitHub Copilot

GitHub Copilot est un outil puissant pour accélérer votre développement. Voici comment l'utiliser efficacement :

### 1️⃣ Soyez précis avec vos **intentions**

L'intention décrit clairement ce que vous voulez réaliser.

**❌ Mauvais (trop vague) :**
```python
# Créer une fonction
def process_data():
    pass
```

**✅ Bon (intention claire) :**
```python
# Fonction pour calculer la moyenne de tous les nombres positifs dans une liste
def calculate_average_positive(numbers):
```

**Exemple du projet :**
```python
# Sauvegarde une opération réussie dans le fichier d'historique avec timestamp
def save_operation(operation, a, b, result):
```

### 2️⃣ Définissez les **contraintes**

Les contraintes précisent les limitations et règles à respecter.

**Intention + Contraintes = Meilleur résultat**

**Exemple dans le projet :**

```python
# Fonction pour afficher l'historique des opérations
# Contraintes:
# - Formater les timestamps en ISO 8601
# - Afficher le symbole de l'opération (+ - * /)
# - Limiter l'affichage si le paramètre 'limit' est fourni
# - Afficher "Aucune opération" si l'historique est vide
def display_history(limit=None):
```

### 3️⃣ Fournissez des **exemples**

Les exemples montrent le comportement attendu de votre code.

**Commentaires avec exemples :**

```python
# Convertir une chaîne convertible en nombre
# Exemples:
# float("2") → 2.0
# float("3.5") → 3.5
# float("-10") → -10.0
a = float(user_input)
```

**Docstrings avec exemples :**

```python
def add(a, b):
    """
    Addition de deux nombres.
    
    Exemples:
        >>> add(5, 3)
        8
        >>> add(-2, 7)
        5
        >>> add(2.5, 1.5)
        4.0
    """
    return a + b
```

### 📋 Formule de prompt efficace

Pour un meilleur résultat, structurez vos demandes ainsi :

```
[Intention]: Créer une fonction pour...
[Contraintes]: 
  - Valider que...
  - Retourner...
  - Gérer les cas où...
[Exemples]:
  - Input: X → Output: Y
  - Input: A → Output: B
```

**Exemple appliqué au projet :**

```
[Intention]: Créer une fonction pour gérer la division de deux nombres

[Contraintes]:
  - Diviser deux nombres flottants
  - Lever une ValueError si le diviseur est zéro
  - Retourner le résultat en tant que float

[Exemples]:
  - div(20, 4) → 5.0
  - div(-10, 2) → -5.0
  - div(5, 0) → ValueError("Erreur : Division par zéro impossible")
```

### 💡 Cas d'usage réels du projet

#### Cas 1 : Créer les fonctions mathématiques

**Bon prompt :**
```
Créer les 4 fonctions mathématiques:
- Fonction add(a,b) pour l'addition
- Fonction sub(a,b) pour la soustraction
- Fonction mul(a, b) pour la multiplication
- Fonction div(a, b) pour la division avec gestion de la division par zéro
Chaque fonction doit avoir une docstring avec exemples
```

#### Cas 2 : Ajouter des commandes spéciales au mode interactif

**Bon prompt :**
```
[Intention]: Ajouter des commandes spéciales au mode interactif

[Contraintes]:
  - Commande 'history': affiche l'historique des opérations
  - Commande 'stats': affiche les statistiques (total et par opération)
  - Commande 'clear': efface l'historique
  - Ces commandes s'exécutent avant le parsing des opérations
  - Utiliser 'continue' pour passer à l'itération suivante

[Exemples]:
  >>> history
  → Affiche toutes les opérations avec timestamps
  >>> stats
  → Affiche: Total: 5, Additions: 2, Divisions: 1...
  >>> clear
  → Affiche: "✓ Historique effacé"
```

#### Cas 3 : Créer une suite de tests

**Bon prompt :**
```
[Intention]: Créer des tests pour tester la fonction division

[Contraintes]:
  - Tester les cas simples (nombres positifs)
  - Tester les nombres négatifs
  - Tester les nombres décimaux
  - Tester la division par zéro (doit lever ValueError)
  - Utiliser pytest
  - Ajouter des docstrings détaillées à chaque test

[Exemples]:
  - div(20, 4) == 5.0 ✓
  - div(-10, 2) == -5.0 ✓
  - div(5, 0) → ValueError ✓
```

### ✅ Checklist pour un bon prompt

Avant de demander à Copilot, vérifiez :

- [ ] **Intention claire** : Qu'est-ce que je veux créer/modifier ?
- [ ] **Contraintes explicites** : Quelles sont les règles ?
- [ ] **Exemples concrets** : Quels sont les cas d'usage ?
- [ ] **Contexte fourni** : Copilot comprend-il le contexte ?
- [ ] **Pas trop long** : Le prompt n'est pas excessivement verbeux
- [ ] **Pas trop court** : Le prompt donne assez d'informations

### 🎯 Avantages de cette approche

✓ **Génération plus précise** : Copilot génère exactement ce que vous avez besoin
✓ **Moins de révisions** : Moins de corrections nécessaires après génération
✓ **Meilleure qualité** : Code mieux structuré et documenté
✓ **Apprentissage** : Vous comprenez mieux ce que vous demandez
✓ **Efficacité** : Gagnez du temps en étant spécifique dès le départ

### 📚 Ressources supplémentaires

- **Documentation Copilot** : https://github.com/features/copilot
- **Prompt Engineering** : https://platform.openai.com/docs/guides/prompt-engineering
- **Best Practices** : https://github.blog/2023-06-20-how-to-write-better-prompts-for-github-copilot/

---

**Dernière mise à jour** : Décembre 2025
