from bs4 import BeautifulSoup


def parser(response):
    soup = BeautifulSoup(response.text, "html.parser")
    result = {}
 
    h1 = soup.h1.string if soup.h1 else None
    title = soup.title.string if soup.title else None
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag:
        meta_description = meta_tag.get("content")
    else:
        meta_description = None
    
    result["h1"] = h1[:255]
    result["title"] = title[:255]
    result["description"] = meta_description[:255]
    
    return result
