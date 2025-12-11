from client_llm.recipe_search import generate_recipe_offline

# Prompt de test
prompt = "Recettes à base de poulet"

# Appel du mode hors ligne
result = generate_recipe_offline(prompt)

print("=== Résultat ===")
print(result)