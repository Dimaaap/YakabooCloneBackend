def short_text_formatter(max_len: int):
    def formatter(model, name):
        text = getattr(model, name)
        if not text:
            return ""
        return text if len(text) <= max_len else text[:max_len] + "..."
    return formatter