import csv
from itertools import combinations


# Étape 1 : Lire le fichier CSV
def read_data(csv_file):
    actions = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cost = float(row["Coût par action (en euros)"])
            if cost > 0:  # Exclure les coûts nuls ou négatifs
                profit = float(
                    row["Bénéfice (après 2 ans)"].replace('%', '')) / 100
                action = {
                    "name": row["Actions"],
                    "cost": cost,
                    "profit": profit
                }
                actions.append(action)
    return actions


# Étape 2 : Générer toutes les combinaisons possibles
def generate_combinations(actions, max_budget):
    n = len(actions)
    best_actions = []
    best_profit = 0

    # Tester toutes les tailles de combinaisons (1 à n actions)
    for r in range(1, n + 1):
        for combination in combinations(actions, r):
            # Étape 3 : Filtrer les combinaisons valides
            total_cost = sum(action["cost"] for action in combination)
            if total_cost <= max_budget:
                # Étape 4 : Calculer le bénéfice total
                total_profit = sum(
                    action["profit"] * action["cost"] for action in combination)
                if total_profit > best_profit:
                    best_actions = combination
                    best_profit = total_profit
    return best_actions, best_profit


# Étape 5 : Afficher la solution
def display_results(best_actions, best_profit):
    total_cost = sum(action["cost"] for action in best_actions)
    print("Meilleure combinaison d'actions :")
    for action in best_actions:
        print(f"- {action['name']} : Coût = {action['cost']
                                             } €, Bénéfice = {action['profit'] * action['cost']} €")
    print(f"Bénéfice total : {best_profit} €")
    print(f"Coût total des actions : {total_cost} €")


# Main
def main():
    csv_file = "liste_actions_p7.csv"
    max_budget = 500
    actions = read_data(csv_file)
    best_actions, best_profit = generate_combinations(
        actions, max_budget)
    display_results(best_actions, best_profit)


if __name__ == "__main__":
    main()
