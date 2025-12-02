import argparse
import sys
from calc import add, sub, mul, div
from calc_storage import save_operation, load_history, display_history, clear_history, get_history_stats


def interactive_mode():
    """Mode interactif pour la calculatrice"""
    print("=" * 50)
    print("Calculatrice - Mode Interactif")
    print("=" * 50)
    print("\nCommandes disponibles: add, sub, mul, div, history, stats, clear, quit")
    print("Syntaxe: <operation> <nombre1> <nombre2>")
    print("Exemple: add 5 3\n")
    
    while True:
        try:
            # Afficher l'invite
            user_input = input(">>> ").strip()
            
            # Vérifier si l'utilisateur veut quitter
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Au revoir!")
                break
            
            # Vérifier que l'input n'est pas vide
            if not user_input:
                continue
            
            # Commandes spéciales
            if user_input.lower() == 'history':
                display_history()
                continue
            elif user_input.lower() == 'stats':
                stats = get_history_stats()
                print(f"\n📊 STATISTIQUES")
                print(f"Total d'opérations: {stats['total']}")
                print(f"Additions: {stats['by_operation']['add']}")
                print(f"Soustractions: {stats['by_operation']['sub']}")
                print(f"Multiplications: {stats['by_operation']['mul']}")
                print(f"Divisions: {stats['by_operation']['div']}\n")
                continue
            elif user_input.lower() == 'clear':
                if clear_history():
                    print("✓ Historique effacé\n")
                continue
            
            # Parser l'input
            parts = user_input.split()
            
            if len(parts) != 3:
                print("❌ Erreur: Format invalide. Utilisez: <operation> <nombre1> <nombre2>")
                print("   Exemple: add 5 3\n")
                continue
            
            command, a_str, b_str = parts
            
            # Convertir les arguments en floats
            try:
                a = float(a_str)
                b = float(b_str)
            except ValueError:
                print(f"❌ Erreur: '{a_str}' ou '{b_str}' n'est pas un nombre valide")
                print("   Utilisez des nombres entiers ou décimaux (ex: 5, 3.14)\n")
                continue
            
            # Exécuter l'opération
            try:
                if command == 'add':
                    result = add(a, b)
                    print(f"✓ Résultat: {a} + {b} = {result:.4f}")
                    save_operation('add', a, b, result)
                    print()
                
                elif command == 'sub':
                    result = sub(a, b)
                    print(f"✓ Résultat: {a} - {b} = {result:.4f}")
                    save_operation('sub', a, b, result)
                    print()
                
                elif command == 'mul':
                    result = mul(a, b)
                    print(f"✓ Résultat: {a} * {b} = {result:.4f}")
                    save_operation('mul', a, b, result)
                    print()
                
                elif command == 'div':
                    result = div(a, b)
                    print(f"✓ Résultat: {a} / {b} = {result:.4f}")
                    save_operation('div', a, b, result)
                    print()
                
                else:
                    print(f"❌ Erreur: Commande '{command}' inconnue")
                    print("   Commandes valides: add, sub, mul, div, history, stats, clear\n")
            
            except ValueError as e:
                print(f"❌ Erreur: {e}\n")
        
        except KeyboardInterrupt:
            print("\n\nAu revoir!")
            break
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}\n")


def cli_mode(args):
    """Mode ligne de commande standard"""
    try:
        result = None
        
        if args.command == 'add':
            result = add(args.a, args.b)
            print(f"{args.a} + {args.b} = {result:.4f}")
            save_operation('add', args.a, args.b, result)
        
        elif args.command == 'sub':
            result = sub(args.a, args.b)
            print(f"{args.a} - {args.b} = {result:.4f}")
            save_operation('sub', args.a, args.b, result)
        
        elif args.command == 'mul':
            result = mul(args.a, args.b)
            print(f"{args.a} * {args.b} = {result:.4f}")
            save_operation('mul', args.a, args.b, result)
        
        elif args.command == 'div':
            result = div(args.a, args.b)
            print(f"{args.a} / {args.b} = {result:.4f}")
            save_operation('div', args.a, args.b, result)
    
    except ValueError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erreur inattendue : {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Interface en ligne de commande pour la calculatrice"""
    parser = argparse.ArgumentParser(
        description='Calculatrice en ligne de commande',
        prog='calc_cli'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')
    
    # Commande add
    add_parser = subparsers.add_parser('add', help='Addition de deux nombres')
    add_parser.add_argument('a', type=float, help='Premier nombre')
    add_parser.add_argument('b', type=float, help='Deuxième nombre')
    
    # Commande sub
    sub_parser = subparsers.add_parser('sub', help='Soustraction de deux nombres')
    sub_parser.add_argument('a', type=float, help='Premier nombre')
    sub_parser.add_argument('b', type=float, help='Deuxième nombre')
    
    # Commande mul
    mul_parser = subparsers.add_parser('mul', help='Multiplication de deux nombres')
    mul_parser.add_argument('a', type=float, help='Premier nombre')
    mul_parser.add_argument('b', type=float, help='Deuxième nombre')
    
    # Commande div
    div_parser = subparsers.add_parser('div', help='Division de deux nombres')
    div_parser.add_argument('a', type=float, help='Dividende')
    div_parser.add_argument('b', type=float, help='Diviseur')
    
    # Commande interactive
    interactive_parser = subparsers.add_parser('interactive', help='Mode interactif')
    
    args = parser.parse_args()
    
    # Si aucune commande n'est fournie, lancer le mode interactif
    if args.command is None or args.command == 'interactive':
        interactive_mode()
    else:
        cli_mode(args)


if __name__ == '__main__':
    main()
