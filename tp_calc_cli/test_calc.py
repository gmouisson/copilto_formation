import pytest
from calc import add, sub, mul, div


# ============================================================================
# TESTS POUR LA FONCTION ADDITION
# ============================================================================

class TestAdd:
    """Tests pour la fonction addition"""
    
    # --- Opérations simples ---
    def test_add_positifs(self):
        """
        Test addition de deux nombres positifs (opération simple).
        Cas: 5 + 3 = 8, 1 + 1 = 2, 100 + 50 = 150
        """
        assert add(5, 3) == 8
        assert add(1, 1) == 2
        assert add(100, 50) == 150
    
    # --- Nombres négatifs ---
    def test_add_negatifs(self):
        """
        Test addition avec nombres négatifs.
        Cas: (-5) + (-3) = -8, (-2) + 7 = 5, 10 + (-4) = 6
        """
        assert add(-5, -3) == -8
        assert add(-2, 7) == 5
        assert add(10, -4) == 6
    
    # --- Nombres flottants ---
    def test_add_decimaux(self):
        """
        Test addition de nombres flottants/décimaux.
        Cas: 2.5 + 1.5 = 4.0, 0.1 + 0.2 ≈ 0.3
        Note: Utilisation de pytest.approx() pour éviter les erreurs d'arrondi
        """
        assert add(2.5, 1.5) == 4.0
        assert add(0.1, 0.2) == pytest.approx(0.3)
    
    # --- Cas limites ---
    def test_add_zero(self):
        """
        Test addition avec zéro (élément neutre).
        Cas: 0 + 5 = 5, 5 + 0 = 5, 0 + 0 = 0
        """
        assert add(0, 5) == 5
        assert add(5, 0) == 5
        assert add(0, 0) == 0
    
    # --- Entrées sous forme de chaînes convertibles ---
    def test_add_strings_convertibles(self):
        """
        Test addition avec des chaînes convertibles en nombres.
        Les fonctions acceptent directement des float, donc les chaînes
        doivent être converties avant d'être passées à la fonction.
        Cas: float("2") + float("3") = 5.0, float("2.5") + float("3.5") = 6.0
        """
        assert add(float("2"), float("3")) == 5.0
        assert add(float("2.5"), float("3.5")) == 6.0
        assert add(float("-1"), float("4")) == 3.0


# ============================================================================
# TESTS POUR LA FONCTION SOUSTRACTION
# ============================================================================

class TestSub:
    """Tests pour la fonction soustraction"""
    
    # --- Opérations simples ---
    def test_sub_positifs(self):
        """
        Test soustraction de deux nombres positifs (opération simple).
        Cas: 10 - 4 = 6, 5 - 5 = 0, 100 - 30 = 70
        """
        assert sub(10, 4) == 6
        assert sub(5, 5) == 0
        assert sub(100, 30) == 70
    
    # --- Nombres négatifs ---
    def test_sub_negatifs(self):
        """
        Test soustraction avec nombres négatifs.
        Cas: 5 - 8 = -3, (-2) - (-5) = 3, (-10) - 5 = -15
        """
        assert sub(5, 8) == -3
        assert sub(-2, -5) == 3
        assert sub(-10, 5) == -15
    
    # --- Nombres flottants ---
    def test_sub_decimaux(self):
        """
        Test soustraction de nombres flottants/décimaux.
        Cas: 7.5 - 2.5 = 5.0, 1.1 - 0.1 ≈ 1.0
        """
        assert sub(7.5, 2.5) == 5.0
        assert sub(1.1, 0.1) == pytest.approx(1.0)
    
    # --- Cas limites ---
    def test_sub_zero(self):
        """
        Test soustraction avec zéro.
        Cas: 5 - 0 = 5, 0 - 5 = -5, 0 - 0 = 0
        """
        assert sub(5, 0) == 5
        assert sub(0, 5) == -5
        assert sub(0, 0) == 0
    
    # --- Entrées sous forme de chaînes convertibles ---
    def test_sub_strings_convertibles(self):
        """
        Test soustraction avec des chaînes convertibles en nombres.
        Les fonctions acceptent directement des float, donc les chaînes
        doivent être converties avant d'être passées à la fonction.
        Cas: float("10") - float("3") = 7.0, float("5.5") - float("2.5") = 3.0
        """
        assert sub(float("10"), float("3")) == 7.0
        assert sub(float("5.5"), float("2.5")) == 3.0
        assert sub(float("-5"), float("-2")) == -3.0


# ============================================================================
# TESTS POUR LA FONCTION MULTIPLICATION
# ============================================================================

class TestMul:
    """Tests pour la fonction multiplication"""
    
    # --- Opérations simples ---
    def test_mul_positifs(self):
        """
        Test multiplication de deux nombres positifs (opération simple).
        Cas: 4 * 5 = 20, 3 * 3 = 9, 10 * 10 = 100
        """
        assert mul(4, 5) == 20
        assert mul(3, 3) == 9
        assert mul(10, 10) == 100
    
    # --- Nombres négatifs ---
    def test_mul_negatifs(self):
        """
        Test multiplication avec nombres négatifs.
        Cas: (-3) * 2 = -6, (-4) * (-5) = 20, (-2) * (-2) = 4
        """
        assert mul(-3, 2) == -6
        assert mul(-4, -5) == 20
        assert mul(-2, -2) == 4
    
    # --- Nombres flottants ---
    def test_mul_decimaux(self):
        """
        Test multiplication de nombres flottants/décimaux.
        Cas: 2.5 * 4 = 10.0, 0.5 * 0.5 = 0.25
        """
        assert mul(2.5, 4) == 10.0
        assert mul(0.5, 0.5) == 0.25
    
    # --- Cas limites ---
    def test_mul_zero(self):
        """
        Test multiplication avec zéro (absorbant).
        Cas: 0 * 5 = 0, 5 * 0 = 0, 0 * 0 = 0
        """
        assert mul(0, 5) == 0
        assert mul(5, 0) == 0
        assert mul(0, 0) == 0
    
    def test_mul_un(self):
        """
        Test multiplication par un (élément neutre).
        Cas: 1 * 5 = 5, 5 * 1 = 5, 1 * 1 = 1
        """
        assert mul(1, 5) == 5
        assert mul(5, 1) == 5
        assert mul(1, 1) == 1
    
    # --- Entrées sous forme de chaînes convertibles ---
    def test_mul_strings_convertibles(self):
        """
        Test multiplication avec des chaînes convertibles en nombres.
        Les fonctions acceptent directement des float, donc les chaînes
        doivent être converties avant d'être passées à la fonction.
        Cas: float("4") * float("5") = 20.0, float("2.5") * float("2") = 5.0
        """
        assert mul(float("4"), float("5")) == 20.0
        assert mul(float("2.5"), float("2")) == 5.0
        assert mul(float("-3"), float("2")) == -6.0


# ============================================================================
# TESTS POUR LA FONCTION DIVISION
# ============================================================================

class TestDiv:
    """Tests pour la fonction division"""
    
    # --- Opérations simples ---
    def test_div_positifs(self):
        """
        Test division de deux nombres positifs (opération simple).
        Cas: 20 / 4 = 5.0, 10 / 2 = 5.0, 15 / 3 = 5.0
        """
        assert div(20, 4) == 5.0
        assert div(10, 2) == 5.0
        assert div(15, 3) == 5.0
    
    # --- Nombres négatifs ---
    def test_div_negatifs(self):
        """
        Test division avec nombres négatifs.
        Cas: (-10) / 2 = -5.0, 10 / (-2) = -5.0, (-20) / (-4) = 5.0
        """
        assert div(-10, 2) == -5.0
        assert div(10, -2) == -5.0
        assert div(-20, -4) == 5.0
    
    # --- Nombres flottants ---
    def test_div_decimaux(self):
        """
        Test division de nombres flottants/décimaux.
        Cas: 7.5 / 2.5 = 3.0, 1 / 2 = 0.5
        """
        assert div(7.5, 2.5) == 3.0
        assert div(1, 2) == 0.5
    
    # --- Division par zéro (DOIT LEVER UNE ERREUR) ---
    def test_div_par_zero(self):
        """
        Test division par zéro (CASE CRITIQUE).
        Doit lever une exception ValueError avec le message approprié.
        Cas: 5 / 0 → ValueError, 0 / 0 → ValueError, (-5) / 0 → ValueError
        """
        # Vérifier que l'exception est levée avec le bon message
        with pytest.raises(ValueError, match="Division par zéro impossible"):
            div(5, 0)
        
        # Test avec zéro au numérateur aussi
        with pytest.raises(ValueError):
            div(0, 0)
        
        # Test avec nombre négatif au numérateur
        with pytest.raises(ValueError):
            div(-5, 0)
    
    # --- Cas limites ---
    def test_div_zero_au_numerateur(self):
        """
        Test division de zéro (zéro divisé par un nombre non-nul).
        Cas: 0 / 5 = 0.0, 0 / 1 = 0.0, 0 / (-3) = 0.0
        """
        assert div(0, 5) == 0.0
        assert div(0, 1) == 0.0
        assert div(0, -3) == 0.0
    
    # --- Entrées sous forme de chaînes convertibles ---
    def test_div_strings_convertibles(self):
        """
        Test division avec des chaînes convertibles en nombres.
        Les fonctions acceptent directement des float, donc les chaînes
        doivent être converties avant d'être passées à la fonction.
        Cas: float("20") / float("4") = 5.0, float("7") / float("2") = 3.5
        """
        assert div(float("20"), float("4")) == 5.0
        assert div(float("7"), float("2")) == 3.5
        assert div(float("-10"), float("2")) == -5.0
    
    # --- Entrées de chaînes convertibles avec division par zéro ---
    def test_div_strings_par_zero(self):
        """
        Test division par zéro avec des chaînes convertibles en nombres.
        Même avec des chaînes converties, la division par zéro doit lever une erreur.
        Cas: float("5") / float("0") → ValueError
        """
        with pytest.raises(ValueError, match="Division par zéro impossible"):
            div(float("5"), float("0"))


# ============================================================================
# TESTS D'INTÉGRATION
# ============================================================================

class TestIntegration:
    """Tests d'intégration combinant plusieurs opérations"""
    
    def test_operations_combinées(self):
        """
        Test combinaison de plusieurs opérations.
        Cas: (10 + 5) * 2 = 30, (20 - 5) / 3 ≈ 5
        """
        # (10 + 5) * 2 = 30
        result = mul(add(10, 5), 2)
        assert result == 30.0
        
        # (20 - 5) / 3 ≈ 5
        result = div(sub(20, 5), 3)
        assert result == pytest.approx(5.0)
    
    def test_associativite_addition(self):
        """
        Test propriété d'associativité de l'addition.
        (a + b) + c == a + (b + c)
        Cas: (10 + 20) + 30 == 10 + (20 + 30) == 60
        """
        a, b, c = 10, 20, 30
        result1 = add(add(a, b), c)
        result2 = add(a, add(b, c))
        assert result1 == result2 == 60
    
    def test_associativite_multiplication(self):
        """
        Test propriété d'associativité de la multiplication.
        (a * b) * c == a * (b * c)
        Cas: (2 * 3) * 4 == 2 * (3 * 4) == 24
        """
        a, b, c = 2, 3, 4
        result1 = mul(mul(a, b), c)
        result2 = mul(a, mul(b, c))
        assert result1 == result2 == 24


# ============================================================================
# TESTS PARAMÉTRÉS (Multiple test cases)
# ============================================================================

class TestParametrises:
    """
    Tests paramétrés pour vérifier plusieurs cas à la fois.
    Permet de tester plusieurs cas similaires avec une seule fonction de test.
    """
    
    @pytest.mark.parametrize("a,b,expected", [
        (1, 1, 2),           # Cas simple
        (5, 3, 8),           # Cas simple
        (-2, 7, 5),          # Nombre négatif
        (0, 0, 0),           # Zéro + zéro
        (2.5, 1.5, 4.0),     # Nombres flottants
    ])
    def test_add_parametrise(self, a, b, expected):
        """
        Test paramétrés pour addition.
        Teste plusieurs cas en une seule exécution.
        """
        assert add(a, b) == expected
    
    @pytest.mark.parametrize("a,b,expected", [
        (10, 4, 6),          # Cas simple
        (5, 8, -3),          # Résultat négatif
        (0, 5, -5),          # Zéro - nombre
        (-5, -2, -3),        # Deux négatifs
        (7.5, 2.5, 5.0),     # Nombres flottants
    ])
    def test_sub_parametrise(self, a, b, expected):
        """
        Test paramétrés pour soustraction.
        Teste plusieurs cas en une seule exécution.
        """
        assert sub(a, b) == expected
    
    @pytest.mark.parametrize("a,b,expected", [
        (4, 5, 20),          # Cas simple
        (-3, 2, -6),         # Nombre négatif
        (0, 10, 0),          # Zéro
        (-4, -5, 20),        # Deux négatifs
        (2.5, 2, 5.0),       # Nombres flottants
    ])
    def test_mul_parametrise(self, a, b, expected):
        """
        Test paramétrés pour multiplication.
        Teste plusieurs cas en une seule exécution.
        """
        assert mul(a, b) == expected
    
    @pytest.mark.parametrize("a,b,expected", [
        (20, 4, 5.0),        # Cas simple
        (-10, 2, -5.0),      # Nombre négatif au numérateur
        (0, 5, 0.0),         # Zéro au numérateur
        (-20, -4, 5.0),      # Deux négatifs
        (7, 2, 3.5),         # Résultat flottant
    ])
    def test_div_parametrise(self, a, b, expected):
        """
        Test paramétrés pour division.
        Teste plusieurs cas en une seule exécution.
        """
        assert div(a, b) == expected
    
    @pytest.mark.parametrize("a,b", [
        (5, 0),              # Nombre positif / zéro
        (0, 0),              # Zéro / zéro
        (-5, 0),             # Nombre négatif / zéro
        (3.5, 0),            # Nombre flottant / zéro
    ])
    def test_div_parametrise_par_zero(self, a, b):
        """
        Test paramétrés pour division par zéro.
        Tous ces cas doivent lever une ValueError.
        """
        with pytest.raises(ValueError, match="Division par zéro impossible"):
            div(a, b)
