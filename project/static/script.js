const apiKey = 'd815bce38aae44e3a97daeb38eb1b50d';
const ingredientsInput = document.getElementById('ingredients');
const recipesDiv = document.getElementById('recipes');
const findRecipesButton = document.getElementById('find-recipes');

findRecipesButton.addEventListener('click', () => {
    const ingredients = ingredientsInput.value.trim();
    if (ingredients) {
        fetchRecipes(ingredients);
    } else {
        alert('Please enter ingredients!');
    }
});

async function fetchRecipes(ingredients) {
    const url = `https://api.spoonacular.com/recipes/findByIngredients?ingredients=${ingredients}&number=5&apiKey=${apiKey}`;

    try {
        const response = await fetch(url);
        const recipes = await response.json();
        displayRecipes(recipes);
    } catch (error) {
        console.error('Error fetching recipes:', error);
    }
}

function displayRecipes(recipes) {
    if (recipes.length === 0) {
        recipesDiv.innerHTML = '<p>No recipes found. Try different ingredients.</p>';
        return;
    }

    recipesDiv.innerHTML = '';

    recipes.forEach(recipe => {
        const recipeElement = document.createElement('div');
        recipeElement.classList.add('recipe');
        recipeElement.innerHTML = `
            <h3>${recipe.title}</h3>
            <p><strong>Used ingredients:</strong> ${recipe.usedIngredientCount}</p>
            <p><strong>Missed ingredients:</strong> ${recipe.missedIngredientCount}</p>
            <a href="https://spoonacular.com/recipes/${recipe.title}-${recipe.id}" target="_blank">View Recipe</a>
        `;
        recipesDiv.appendChild(recipeElement);
    });
}
