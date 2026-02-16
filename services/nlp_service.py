import spacy
from services.portion_service import get_portion_multiplier
from services.portion_service import PORTION_MULTIPLIERS

MEASUREMENT_WORDS = {
    "plate", "bowl", "slice", "cup", "gram", "kg", "piece"
}

nlp = spacy.load("en_core_web_sm")

# Map word numbers to digits
WORD_NUMBERS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10
}

def extract_food_items(text: str):
    doc = nlp(text.lower())

    food_items = []
    quantity = 1
    portion_multiplier = 1

    for token in doc:

        if token.like_num:
            if token.text.isdigit():
                quantity = int(token.text)
            elif token.text in WORD_NUMBERS:
                quantity = WORD_NUMBERS[token.text]

        elif token.text in PORTION_MULTIPLIERS:
            portion_multiplier = get_portion_multiplier(token.text)

        elif token.pos_ == "NOUN" and token.lemma_ not in MEASUREMENT_WORDS:
            final_quantity = quantity * portion_multiplier

            food_items.append({
                "food": token.lemma_,
                "quantity": final_quantity
            })

            quantity = 1
            portion_multiplier = 1

    return food_items
