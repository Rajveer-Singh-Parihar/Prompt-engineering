# Simple Recipe Book in Python

# Dictionary to store recipes
recipe_book = {}

def display_menu():
    """Display the menu options for the user."""
    print("\n===== Recipe Book Menu =====")
    print("1. Add a Recipe")
    print("2. View All Recipes")
    print("3. Search for a Recipe")
    print("4. Exit")

def add_recipe():
    """Add a new recipe to the recipe book."""
    name = input("Enter the recipe name: ").strip()
    ingredients = input("Enter the ingredients (comma-separated): ").strip()
    steps = input("Enter the steps to prepare the recipe: ").strip()
    
    # Store recipe details in the dictionary
    recipe_book[name] = {
        "ingredients": ingredients,
        "steps": steps
    }
    print(f"✅ Recipe '{name}' added successfully!")

def view_recipes():
    """Display all recipes in the recipe book."""
    if not recipe_book:
        print("❗ No recipes found. Add some recipes first!")
    else:
        print("\n📖 All Recipes:")
        for index, recipe_name in enumerate(recipe_book, start=1):
            print(f"{index}. {recipe_name}")

def search_recipe():
    """Search for a recipe by name."""
    if not recipe_book:
        print("❗ No recipes found. Add some recipes first!")
        return
    
    name = input("Enter the recipe name to search: ").strip()
    if name in recipe_book:
        print(f"\n📋 Recipe: {name}")
        print(f"Ingredients: {recipe_book[name]['ingredients']}")
        print(f"Steps: {recipe_book[name]['steps']}")
    else:
        print(f"❌ Recipe '{name}' not found!")

# Main program loop
while True:
    display_menu()
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == "1":
        add_recipe()
    elif choice == "2":
        view_recipes()
    elif choice == "3":
        search_recipe()
    elif choice == "4":
        print("👋 Exiting the Recipe Book. Goodbye!")
        break
    else:
        print("❌ Invalid choice. Please enter a number between 1 and 4.")
