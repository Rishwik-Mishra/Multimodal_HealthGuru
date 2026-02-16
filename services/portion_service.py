PORTION_MULTIPLIERS = {
    "half": 0.5,
    "quarter": 0.25,
    "double": 2,
    "bowl": 1.5,
    "plate": 2,
    "slice": 0.5,
    "cup": 1.2
}

def get_portion_multiplier(token_text):
    return PORTION_MULTIPLIERS.get(token_text, 1)
