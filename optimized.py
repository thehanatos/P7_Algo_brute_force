import csv


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


# Étape 2 : Résoudre avec programmation dynamique
def knapsack_optimized(actions, max_budget):
    n = len(actions)
    # Initialiser la table dynamique (dimensions : (n+1) x (max_budget+1))
    dp = [[0 for _ in range(max_budget + 1)] for _ in range(n + 1)]

    # Remplir la table
    for i in range(1, n + 1):
        for b in range(max_budget + 1):
            dp[i][b] = dp[i - 1][b]
            action_cost = int(actions[i - 1]["cost"])
            action_profit = actions[i - 1]["profit"] * actions[i - 1]["cost"]
            if action_cost <= b:
                dp[i][b] = max(dp[i][b], dp[i - 1]
                               [b - action_cost] + action_profit)

    # Reconstituer la solution optimale
    best_actions = []
    b = max_budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:  # Si l'action a été incluse
            best_actions.append(actions[i - 1])
            b -= int(actions[i - 1]["cost"])

    best_profit = dp[n][max_budget]
    return best_actions, best_profit


# Étape 3 : Afficher la solution
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
    best_actions, best_profit = knapsack_optimized(actions, max_budget)
    display_results(best_actions, best_profit)


if __name__ == "__main__":
    main()
