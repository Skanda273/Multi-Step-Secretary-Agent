def parse_instruction(text):
    text = text.lower()

    if "open" in text:
        return {"action": "open", "target": text.replace("open", "").strip()}

    if "search" in text:
        return {"action": "search", "query": text.replace("search", "").strip()}

    if "click" in text:
        return {"action": "click", "target": text.replace("click", "").strip()}

    return {"action": "unknown", "text": text}