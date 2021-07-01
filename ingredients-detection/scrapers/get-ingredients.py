import json

with open('recipes.json') as file:
  recipes = json.load(file)

a = 0
for recipe in recipes:
        for item in recipe["ingredients"]:
            if "ingredient" in item:
                with open("ingredients.txt", "a+") as file:
                    file.write(item["ingredient"] + "\n")