import csv
from decimal import Decimal
import numpy as np


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
def knapsack_numpy(actions, max_budget):
    n = len(actions)
    max_budget_cents = int(max_budget * 100)

    # Table dynamique
    dp = np.zeros(max_budget_cents + 1)
    selected_actions = [[] for _ in range(max_budget_cents + 1)]

    # Remplir la table dynamique
    for action in actions:
        action_cost_cents = int(round(float(action["cost"]) * 100))
        action_profit = float(action["profit"]) * float(action["cost"])

        # Parcourir la table de manière descendante pour éviter de réutiliser plusieurs fois la même action
        for budget in range(max_budget_cents, action_cost_cents - 1, -1):
            if dp[budget - action_cost_cents] + action_profit > dp[budget]:
                dp[budget] = dp[budget - action_cost_cents] + action_profit
                selected_actions[budget] = selected_actions[budget -
                                                            action_cost_cents] + [action]

    # Reconstituer la solution optimale
    best_budget = max_budget_cents
    best_actions = selected_actions[best_budget]
    total_cost = sum(action["cost"] for action in best_actions)
    best_profit = dp[max_budget_cents]

    return best_actions, total_cost, best_profit


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
    csv_file = "dataset2_p7.csv"
    max_budget = Decimal("500")
    actions = read_data(csv_file)
    best_actions, total_cost, best_profit = knapsack_numpy(
        actions, max_budget)

    display_results(best_actions, best_profit, max_budget)


if __name__ == "__main__":
    main()
