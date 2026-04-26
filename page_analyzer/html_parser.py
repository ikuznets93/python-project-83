from bs4 import BeautifulSoup


def get_tag_text(tag):
    if not tag:
        return None

    text = tag.get_text(strip=True)
    return text[:255] if text else None


def parser(response):
    soup = BeautifulSoup(response.text, "html.parser")
    result = {}
 
    h1 = get_tag_text(soup.h1)
    title = get_tag_text(soup.title)
    meta_tag = soup.find("meta", attrs={"name": "description"})
    meta_content = meta_tag.get("content") if meta_tag else None
    if meta_content:
        meta_description = meta_content[:255]
    else:
        meta_description = None
    
    result["h1"] = h1
    result["title"] = title
    result["description"] = meta_description
    
    return result
