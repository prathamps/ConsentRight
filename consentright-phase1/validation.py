import re
def validate_symptom_input(user_input):
    result = {"valid": False, "cleaned_input": "", "error_message": ""}
    if not user_input or len(user_input.strip()) == 0:
        result["error_message"] = "Please enter a description of your symptoms."
        return result
    cleaned = user_input.strip()
    if len(cleaned) < 5:
        result["error_message"] = "Please provide a more detailed description (at least 5 characters)."
        return result
    if len(cleaned) > 2000:
        result["error_message"] = "Description is too long. Keep it under 2000 characters."
        return result
    if has_excessive_repetition(cleaned):
        result["error_message"] = "Please avoid excessive repetition."
        return result
    if not re.match(r'^[a-zA-Z0-9\s\.,;:!\-\'"()\[\]/+*&%$#@]+$', cleaned):
        result["error_message"] = "Use only standard characters."
        return result
    cleaned = re.sub(r'\s+', ' ', cleaned)
    if not re.search(r'[a-zA-Z]', cleaned):
        result["error_message"] = "Include descriptive text about your symptoms."
        return result
    result["valid"] = True
    result["cleaned_input"] = cleaned
    return result

def has_excessive_repetition(text):
    if re.search(r'(.)\1{4,}', text):
        return True
    words = text.lower().split()
    word_counts = {}
    for word in words:
        if len(word) > 2:
            word_counts[word] = word_counts.get(word, 0) + 1
            if word_counts[word] > 10:
                return True
    return False

