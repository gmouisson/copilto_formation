def add(a, b):
    """
    Addition de deux nombres.
    
    Args:
        a: Premier nombre
        b: Deuxième nombre
    
    Returns:
        La somme de a et b
    
    Exemples:
        >>> add(5, 3)
        8
        >>> add(-2, 7)
        5
        >>> add(2.5, 1.5)
        4.0
    """
    return a + b


def sub(a, b):
    """
    Soustraction de deux nombres.
    
    Args:
        a: Premier nombre
        b: Deuxième nombre
    
    Returns:
        La différence a - b
    
    Exemples:
        >>> sub(10, 4)
        6
        >>> sub(5, 8)
        -3
        >>> sub(7.5, 2.5)
        5.0
    """
    return a - b


def mul(a, b):
    """
    Multiplication de deux nombres.
    
    Args:
        a: Premier nombre
        b: Deuxième nombre
    
    Returns:
        Le produit de a et b
    
    Exemples:
        >>> mul(4, 5)
        20
        >>> mul(-3, 2)
        -6
        >>> mul(2.5, 4)
        10.0
    """
    return a * b


def div(a, b):
    """
    Division de deux nombres avec gestion de la division par zéro.
    
    Args:
        a: Dividende
        b: Diviseur
    
    Returns:
        Le quotient a / b
    
    Raises:
        ValueError: Si le diviseur b est égal à zéro
    
    Exemples:
        >>> div(20, 4)
        5.0
        >>> div(7, 2)
        3.5
        >>> div(-10, 2)
        -5.0
        >>> div(5, 0)
        Traceback (most recent call last):
            ...
        ValueError: Erreur : Division par zéro impossible
    """
    if b == 0:
        raise ValueError("Erreur : Division par zéro impossible")
    return a / b
