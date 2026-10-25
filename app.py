
import streamlit as st
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama


# --------------------------------------------------
# 1. RECIPE DATABASE
# --------------------------------------------------

RECIPES = {
    "Potato Tomato Curry": {
        "ingredients": [
            "potato", "tomato", "onion", "oil",
            "salt", "turmeric", "chilli powder"
        ],
        "steps": [
            "Wash, peel, and cut the potatoes.",
            "Heat oil in a pan and cook chopped onion until soft.",
            "Add chopped tomato, salt, turmeric, and chilli powder.",
            "Cook until the tomato becomes soft.",
            "Add potato and enough water for the desired gravy.",
            "Cover and cook until the potato is completely tender."
        ],
        "time": "25-30 minutes",
        "type": "vegetarian"
    },

    "Baingan Masala (Eggplant Curry)": {
        "ingredients": [
            "eggplant", "onion", "tomato", "oil",
            "salt", "turmeric", "chilli powder"
        ],
        "steps": [
            "Wash and cut the eggplant into small pieces.",
            "Heat oil and cook chopped onion until soft.",
            "Add tomato, salt, turmeric, and chilli powder.",
            "Add eggplant and mix well.",
            "Cover and cook until the eggplant is completely soft.",
            "Add a little water if you want a gravy."
        ],
        "time": "20-25 minutes",
        "type": "vegetarian"
    },

    "Simple Egg Curry": {
        "ingredients": [
            "egg", "onion", "tomato", "oil",
            "salt", "turmeric", "chilli powder"
        ],
        "steps": [
            "Boil the eggs until fully cooked, then peel them.",
            "Heat oil in a pan and cook chopped onion.",
            "Add tomato, salt, turmeric, and chilli powder.",
            "Cook until the tomato softens and forms a masala.",
            "Add a little water and simmer to make gravy.",
            "Add the peeled eggs and simmer for 5 minutes."
        ],
        "time": "20-25 minutes",
        "type": "egg"
    },

    "Aloo Baingan": {
        "ingredients": [
            "potato", "eggplant", "onion", "tomato",
            "oil", "salt", "turmeric", "chilli powder"
        ],
        "steps": [
            "Cut the potato and eggplant into small pieces.",
            "Heat oil and cook chopped onion.",
            "Add tomato and your spices.",
            "Add potato and cook for a few minutes.",
            "Add eggplant and mix everything together.",
            "Cover and cook until both vegetables are fully tender."
        ],
        "time": "25-30 minutes",
        "type": "vegetarian"
    },

    "Tomato Egg Bhurji": {
        "ingredients": [
            "egg", "tomato", "onion", "oil", "salt", "chilli"
        ],
        "steps": [
            "Heat oil in a pan.",
            "Add chopped onion and cook until soft.",
            "Add chopped tomato, salt, and chilli.",
            "Cook until the tomato softens.",
            "Beat the eggs in a bowl and add them to the pan.",
            "Stir until the eggs are fully cooked."
        ],
        "time": "10-15 minutes",
        "type": "egg"
    },

    "Onion Tomato Rice": {
        "ingredients": [
            "rice", "onion", "tomato", "oil",
            "salt", "chilli powder"
        ],
        "steps": [
            "Rinse the rice and cook it until tender.",
            "Heat oil in a pan and cook chopped onion.",
            "Add tomato, salt, and chilli powder.",
            "Cook until the tomato softens.",
            "Add the cooked rice and mix gently.",
            "Heat everything together for a few minutes."
        ],
        "time": "20-30 minutes",
        "type": "vegetarian"
    },

    "Potato Fry": {
        "ingredients": [
            "potato", "oil", "salt", "turmeric", "chilli powder"
        ],
        "steps": [
            "Wash, peel, and cut the potato into small pieces.",
            "Heat oil in a pan.",
            "Add the potato, salt, turmeric, and chilli powder.",
            "Mix well and cook on medium-low heat.",
            "Stir occasionally until the potato is fully cooked and lightly crisp."
        ],
        "time": "20-25 minutes",
        "type": "vegetarian"
    },

    "Boiled Egg Masala": {
        "ingredients": [
            "egg", "onion", "tomato", "oil",
            "salt", "turmeric", "chilli powder"
        ],
        "steps": [
            "Boil the eggs until fully cooked and peel them.",
            "Heat oil and cook chopped onion.",
            "Add tomato and the spices.",
            "Cook until a thick masala forms.",
            "Add the eggs and coat them with the masala.",
            "Cook for another 3-5 minutes."
        ],
        "time": "20 minutes",
        "type": "egg"
    },

    "Basic Vegetable Pulao": {
        "ingredients": [
            "rice", "potato", "onion", "oil", "salt"
        ],
        "steps": [
            "Rinse the rice.",
            "Heat oil in a suitable cooking pot and cook the onion.",
            "Add chopped potato and salt.",
            "Add the rinsed rice and water in the amount suitable for your rice and cooking method.",
            "Cook covered until the rice and potato are fully cooked."
        ],
        "time": "25-35 minutes",
        "type": "vegetarian"
    },

    "Simple Tomato Chutney": {
        "ingredients": [
            "tomato", "onion", "oil", "salt", "chilli"
        ],
        "steps": [
            "Heat a little oil in a pan.",
            "Cook chopped onion until soft.",
            "Add chopped tomato, salt, and chilli.",
            "Cook until everything becomes soft.",
            "Cool slightly and mash or blend if desired."
        ],
        "time": "10-15 minutes",
        "type": "vegetarian"
    }
}


# --------------------------------------------------
# 2. INGREDIENT HELPERS
# --------------------------------------------------

ALIASES = {
    "potatoes": "potato",
    "tomatoes": "tomato",
    "onions": "onion",
    "eggs": "egg",
    "brinjal": "eggplant",
    "aubergine": "eggplant",
    "baingan": "eggplant",
    "chillies": "chilli",
    "chilies": "chilli",
    "green chilli": "chilli",
    "green chillies": "chilli",
    "red chilli": "chilli",
    "red chillies": "chilli",
    "chili powder": "chilli powder",
    "red chilli powder": "chilli powder",
    "oil": "oil",
    "cooking oil": "oil",
    "rice": "rice",
    "salt": "salt",
    "turmeric powder": "turmeric",
    "haldi": "turmeric",
    "dhania powder": "coriander powder",
    "coriander powder": "coriander powder",
    "garam masala": "garam masala",
    "ginger garlic paste": "ginger garlic paste"
}


def normalize_ingredients(text):
    items = [item.strip().lower() for item in text.split(",")]
    cleaned = []

    for item in items:
        if not item:
            continue

        cleaned.append(ALIASES.get(item, item))

    return set(cleaned)


# --------------------------------------------------
# 3. AGENT TOOL: FIND RECIPES
# --------------------------------------------------

@tool
def find_recipe_ideas(
    available_ingredients: str,
    dietary_preference: str = "any"
) -> str:
    """Find recipes from the recipe collection using ingredients the user has.
    available_ingredients must be a comma-separated list.
    dietary_preference can be any, vegetarian, or egg.
    Return matching dishes and the ingredients that are missing.
    """
    available = normalize_ingredients(available_ingredients)
    preference = dietary_preference.strip().lower()

    matches = []

    for name, recipe in RECIPES.items():
        if preference == "vegetarian" and recipe["type"] != "vegetarian":
            continue

        if preference == "egg" and recipe["type"] != "egg":
            continue

        required = set(recipe["ingredients"])
        matched = required.intersection(available)
        missing = required - available

        if not matched:
            continue

        score = len(matched) / len(required)

        # Prioritize recipes using most available ingredients.
        matches.append(
            (score, len(matched), name, sorted(matched), sorted(missing))
        )

    matches.sort(key=lambda item: (item[0], item[1]), reverse=True)

    if not matches:
        return (
            "No matching recipe was found in the built-in collection. "
            "Ask the model to suggest a simple alternative, clearly "
            "labelled as a general suggestion."
        )

    output = ["Matching recipes from the built-in collection:"]

    for score, count, name, matched, missing in matches[:6]:
        output.append(
            f"\nDish: {name}\n"
            f"Matching ingredients: {', '.join(matched)}\n"
            f"Missing ingredients: {', '.join(missing) if missing else 'None'}\n"
            f"Ingredient match: {round(score * 100)}%\n"
            f"Cooking time: {RECIPES[name]['time']}"
        )

    return "\n".join(output)


# --------------------------------------------------
# 4. AGENT TOOL: CHECK MISSING INGREDIENTS
# --------------------------------------------------

@tool
def check_missing_ingredients(
    recipe_name: str,
    available_ingredients: str
) -> str:
    """Check which ingredients are missing for a named recipe.
    Use a recipe name from the built-in recipe collection.
    """
    available = normalize_ingredients(available_ingredients)

    for name, recipe in RECIPES.items():
        if name.lower() == recipe_name.strip().lower():
            required = set(recipe["ingredients"])
            missing = sorted(required - available)
            present = sorted(required.intersection(available))

            return (
                f"Recipe: {name}\n"
                f"Available required ingredients: "
                f"{', '.join(present) if present else 'None'}\n"
                f"Missing ingredients: "
                f"{', '.join(missing) if missing else 'None'}"
            )

    return (
        "Recipe not found in the built-in collection. "
        "Use find_recipe_ideas to see supported recipes."
    )


# --------------------------------------------------
# 5. AGENT TOOL: GET COOKING STEPS
# --------------------------------------------------

@tool
def get_recipe_details(recipe_name: str) -> str:
    """Return the ingredients, cooking time, and step-by-step method
    for a recipe in the built-in recipe collection.
    """
    for name, recipe in RECIPES.items():
        if name.lower() == recipe_name.strip().lower():
            steps = "\n".join(
                f"{i + 1}. {step}"
                for i, step in enumerate(recipe["steps"])
            )

            return (
                f"Recipe: {name}\n"
                f"Ingredients: {', '.join(recipe['ingredients'])}\n"
                f"Cooking time: {recipe['time']}\n"
                f"Method:\n{steps}"
            )

    return (
        "Recipe not found. First use find_recipe_ideas to discover "
        "recipes in the collection."
    )


# --------------------------------------------------
# 6. CREATE THE LOCAL AI AGENT
# --------------------------------------------------

@st.cache_resource
def create_cooking_agent():
    model = ChatOllama(
        model="llama3.2:3b",
        temperature=0.2
    )

    tools = [
        find_recipe_ideas,
        check_missing_ingredients,
        get_recipe_details
    ]

    return create_agent(
        model=model,
        tools=tools,
        system_prompt="""
You are a helpful home cooking assistant.

Your job is to suggest dishes using ingredients the user already has.

Rules:
1. Understand the user's ingredient list before answering.
2. Use find_recipe_ideas when the user asks what they can cook.
3. Never claim that a dish is from the built-in collection unless the
   tool actually returned it.
4. Explain which ingredients are available and which are missing.
5. Prefer recipes that use the ingredients the user already has.
6. Ask about dietary preferences only when necessary.
7. If the user requests a specific recipe, use get_recipe_details
   when that recipe is in the collection.
8. Give numbered cooking steps in simple language.
9. Do not claim an ingredient is available unless the user listed it.
10. You may offer a clearly labelled general recipe suggestion if
    the built-in collection has no suitable match. Do not pretend
    that the suggestion came from the recipe database.
11. Remind the user to cook eggs and other perishable ingredients
    thoroughly.
12. Be friendly, practical, and concise.
"""
    )


# --------------------------------------------------
# 7. STREAMLIT USER INTERFACE
# --------------------------------------------------

st.set_page_config(
    page_title="Local AI Cooking Agent",
    page_icon="🍳",
    layout="centered"
)

st.title("🍳 Local AI Cooking Agent")
st.write(
    "Tell me what ingredients you have at home, "
    "and I will help you decide what to cook."
)

st.caption("Powered by a local Ollama model")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "ingredients" not in st.session_state:
    st.session_state.ingredients = ""

with st.sidebar:
    st.header("🥕 Your ingredients")

    ingredients = st.text_area(
        "Enter ingredients separated by commas",
        value=st.session_state.ingredients,
        placeholder=(
            "onion, tomato, potato, eggplant, egg, rice, salt"
        ),
        height=140
    )

    st.session_state.ingredients = ingredients

    st.info(
        "Include spices, oil, rice, flour, or other staples "
        "if you have them."
    )

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
user_prompt = st.chat_input(
    "What can I cook with these ingredients?"
)

if user_prompt:
    if not st.session_state.ingredients.strip():
        st.warning(
            "Please enter your available ingredients in the sidebar first."
        )
    else:
        combined_prompt = (
            f"My available ingredients are: "
            f"{st.session_state.ingredients}.\n\n"
            f"My request: {user_prompt}"
        )

        st.session_state.messages.append(
            {"role": "user", "content": user_prompt}
        )

        with st.chat_message("user"):
            st.markdown(user_prompt)

        try:
            agent = create_cooking_agent()

            # Include the ingredient list in the current user message.
            # Keep prior visible chat messages for conversation context.
            agent_messages = [
                {
                    "role": message["role"],
                    "content": message["content"]
                }
                for message in st.session_state.messages[:-1]
            ]
            agent_messages.append(
                {"role": "user", "content": combined_prompt}
            )

            with st.chat_message("assistant"):
                with st.spinner("Finding suitable recipes..."):
                    result = agent.invoke(
                        {"messages": agent_messages}
                    )

                    answer = result["messages"][-1].content

                    if not isinstance(answer, str):
                        answer = str(answer)

                st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as error:
            st.error(
                "The agent could not complete the request. "
                "Check that Ollama is running and the model is installed."
            )
            st.code(str(error))
