from urllib.parse import urlparse

import validators


def normalize_url(url: str) -> str:
    parsed_url = urlparse(url)

    hostname = parsed_url.hostname
    if hostname.startswith("www."):
        hostname = hostname[4:]

    normalized_url = f"{parsed_url.scheme}://{hostname}"
    return normalized_url


def validate_url(url):
    errors = {}

    if not validators.url(url):
        errors["url"] = "Некоректный формат URL"
    if url == "":
        errors["url"] = "URL не может быть пустым"
    if len(url) > 255:
        errors["url"] = "Слишком длинный URL (должен быть меньше 255 символов)"
    
    return errors