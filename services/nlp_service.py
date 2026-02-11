import spacy

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

    for token in doc:

        # Handle numeric digits
        if token.like_num:
            if token.text.isdigit():
                quantity = int(token.text)
            elif token.text in WORD_NUMBERS:
                quantity = WORD_NUMBERS[token.text]
            else:
                quantity = 1

        # Handle nouns (food words)
        elif token.pos_ == "NOUN":
            food_items.append({
                "food": token.lemma_,
                "quantity": quantity
            })
            quantity = 1

    return food_items
