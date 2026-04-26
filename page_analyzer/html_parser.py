from bs4 import BeautifulSoup


def parser(response):
    soup = BeautifulSoup(response.text, "html.parser")
    result = {}
 
    h1 = soup.h1.string[:255] if soup.h1 else None
    title = soup.title.string[:255] if soup.title else None
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag:
        meta_description = meta_tag.get("content")[:255]
    else:
        meta_description = None
    
    result["h1"] = h1
    result["title"] = title
    result["description"] = meta_description
    
    return result
