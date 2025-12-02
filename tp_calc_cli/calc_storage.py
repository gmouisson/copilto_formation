import json
import os
from datetime import datetime


# Chemin vers le fichier d'historique
HISTORY_FILE = "calc_history.json"


def save_operation(operation, a, b, result):
    """
    Sauvegarde une opération réussie dans le fichier d'historique.
    
    Args:
        operation (str): L'opération effectuée (add, sub, mul, div)
        a (float): Premier operande
        b (float): Deuxième operande
        result (float): Résultat de l'opération
    
    Returns:
        bool: True si l'opération a été sauvegardée, False sinon
    
    Exemple:
        >>> save_operation('add', 5, 3, 8)
        True
    """
    try:
        # Charger l'historique existant
        history = load_history()
        
        # Créer une nouvelle entrée
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "operand_a": a,
            "operand_b": b,
            "result": result
        }
        
        # Ajouter à l'historique
        history.append(entry)
        
        # Sauvegarder le fichier
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        
        return True
    
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}")
        return False


def load_history():
    """
    Charge l'historique depuis le fichier JSON.
    
    Returns:
        list: Liste des opérations sauvegardées, ou liste vide si le fichier n'existe pas
    
    Exemple:
        >>> history = load_history()
        >>> isinstance(history, list)
        True
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
            return history if isinstance(history, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def display_history(limit=None):
    """
    Affiche l'historique des opérations de manière formatée.
    
    Args:
        limit (int, optional): Limite le nombre d'opérations affichées. 
                              Si None, affiche tout l'historique.
    
    Returns:
        None
    
    Exemple:
        >>> display_history(5)  # Affiche les 5 dernières opérations
    """
    history = load_history()
    
    if not history:
        print("Aucune opération en historique.")
        return
    
    # Limiter l'affichage si nécessaire
    if limit:
        history = history[-limit:]
    
    print("\n" + "=" * 70)
    print("HISTORIQUE DES OPÉRATIONS")
    print("=" * 70)
    
    for i, entry in enumerate(history, 1):
        timestamp = entry.get("timestamp", "N/A")
        operation = entry.get("operation", "N/A")
        a = entry.get("operand_a", "N/A")
        b = entry.get("operand_b", "N/A")
        result = entry.get("result", "N/A")
        
        # Formater l'opération
        op_symbol = {
            'add': '+',
            'sub': '-',
            'mul': '*',
            'div': '/'
        }.get(operation, operation)
        
        print(f"\n{i}. [{timestamp}]")
        print(f"   Opération: {a} {op_symbol} {b} = {result:.4f}")


def clear_history():
    """
    Efface tout l'historique.
    
    Returns:
        bool: True si l'historique a été effacé, False sinon
    
    Exemple:
        >>> clear_history()
        True
    """
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        return True
    except Exception as e:
        print(f"Erreur lors de la suppression de l'historique: {e}")
        return False


def get_history_stats():
    """
    Retourne des statistiques sur l'historique.
    
    Returns:
        dict: Dictionnaire contenant les statistiques
              (total d'opérations, opérations par type, etc.)
    
    Exemple:
        >>> stats = get_history_stats()
        >>> 'total' in stats
        True
    """
    history = load_history()
    
    stats = {
        'total': len(history),
        'by_operation': {
            'add': 0,
            'sub': 0,
            'mul': 0,
            'div': 0
        }
    }
    
    for entry in history:
        operation = entry.get('operation', '')
        if operation in stats['by_operation']:
            stats['by_operation'][operation] += 1
    
    return stats
