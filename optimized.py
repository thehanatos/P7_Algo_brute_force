import csv
from decimal import Decimal


# Étape 1 : Lire le fichier CSV
def read_data(csv_file):
    actions = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cost = Decimal(row["price"])
            if cost > 0:  # Exclure les coûts nuls ou négatifs
                profit = Decimal(row["profit"].replace('%', '')) / 100
                action = {
                    "name": row["name"],
                    "cost": cost,
                    "profit": profit
                }
                actions.append(action)
    return actions


# Étape 2 : Résoudre avec programmation dynamique
def knapsack_optimized(actions, max_budget):
    n = len(actions)
    max_budget_cents = int(max_budget * 100)  # Convertir en centimes

    # Initialiser la table dynamique (dimensions : (n+1) x (max_budget+1))
    dp = [[0 for _ in range(max_budget_cents + 1)] for _ in range(n + 1)]

    # Remplir la table
    for i in range(1, n + 1):
        for b in range(max_budget_cents + 1):
            dp[i][b] = dp[i - 1][b]
            action_cost_cents = int(
                actions[i - 1]["cost"] * 100)  # En centimes
            action_profit = actions[i - 1]["profit"] * actions[i - 1]["cost"]
            if action_cost_cents <= b:
                dp[i][b] = max(dp[i][b], dp[i - 1]
                               [b - action_cost_cents] + float(action_profit))

    # Reconstituer la solution optimale
    best_actions = []
    b = max_budget_cents
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:  # Si l'action a été incluse
            best_actions.append(actions[i - 1])
            b -= int(actions[i - 1]["cost"] * 100)  # En centimes

    best_profit = dp[n][max_budget_cents]
    return best_actions, best_profit


# Étape 3 : Afficher la solution
def display_results(best_actions, best_profit, max_budget):
    total_cost = sum(action["cost"] for action in best_actions)
    print("Meilleure combinaison d'actions :")
    for action in best_actions:
        print(f"- {action['name']} : Coût = {action['cost']
                                             } €, Bénéfice = {action['profit'] * action['cost']} €")
    print(f"Bénéfice total : {best_profit} €")
    print(f"Coût total des actions : {total_cost} €")
    if total_cost > max_budget:
        print(f"Attention : le coût total dépasse le budget maximal ({
              total_cost} > {max_budget})")


# Main
def main():
    csv_file = "dataset1_p7.csv"
    max_budget = Decimal("500")
    actions = read_data(csv_file)
    best_actions, best_profit = knapsack_optimized(actions, max_budget)
    display_results(best_actions, best_profit, max_budget)


if __name__ == "__main__":
    main()
