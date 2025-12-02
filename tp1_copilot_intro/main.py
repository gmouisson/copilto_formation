# Ecrire une fonction sum_list(nums:list(int)) -> int qui retourne la somme des éléments
#Implémenter sans utiliser la fonction built-in sum.
# Ajouter des commentaires ligne par ligne pour expliquer la logique aux débutants.
def sum_list(nums: list[int]) -> int:
    total = 0  # Initialiser la variable total à 0 pour stocker la somme
    for num in nums:  # Parcourir chaque élément dans la liste nums
        total += num  # Ajouter l'élément courant à la variable total
    return total  # Retourner la somme totale des éléments

# Parcourir une liste [1, 2, 3, 4, 5] et afficher chaque carré
# Transformer en fonction squares (nums: list[int]) -> list[int]
def squares(nums: list[int]) -> list[int]:
    result = []  # Initialiser une liste vide pour stocker les carrés
    for number in nums:  # Parcourir chaque nombre dans la liste
        square = number ** 2  # Calculer le carré du nombre courant
        result.append(square)  # Ajouter le carré à la liste result
    return result  # Retourner la liste des carrés


# Écrire une fonction qui respecte les conventions PEP8 et ajoute des annotations de type
def multiply_elements(elements: list[int], factor: int) -> list[int]:
    """Multiplie chaque élément de la liste par un facteur donné.

    Args:
        elements (list[int]): La liste des entiers à multiplier.
        factor (int): Le facteur par lequel multiplier chaque élément.

    Returns:
        list[int]: Une nouvelle liste contenant les éléments multipliés.
    """
    multiplied = []  # Initialiser une liste vide pour stocker les résultats
    for element in elements:  # Parcourir chaque élément dans la liste
        multiplied_element = element * factor  # Multiplier l'élément par le facteur
        multiplied.append(multiplied_element)  # Ajouter le résultat à la liste
    return multiplied  # Retourner la liste des éléments multipliés

if __name__ == "__main__":
    print(sum_list([1, 2, 3])) # attendu: 6
    print(squares([1, 2, 3, 4])) # attendu: [1, 4, 9, 16]
    print(multiply_elements([1, 2, 3], 3)) # attendu: [3, 6, 9]