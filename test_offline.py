from client_llm.local_search import search_recipes_offline

# Prompt de test
ingredient = "poulet"  # ou tout autre ingrédient

# Appel du mode hors ligne
result = search_recipes_offline(ingredient)

print("=== Résultat ===")
for r in result:
    print(f"Nom: {r[0]}\nIngrédients: {r[1]}\nInstructions: {r[2]}\n{'-'*40}")