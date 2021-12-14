from typing import Optional, TypeGuard
from bs4 import BeautifulSoup
import requests
import urllib.parse

def get_img_urls(url: str, selector: Optional[str]=None) -> list[str]:
    response = requests.get(url)
    paths = get_img_srcs(response.text, selector)
    return [urllib.parse.urljoin(response.url, path) for path in paths]


def is_attr_str(obj: str | list[str] | None) -> TypeGuard[str]:
    return isinstance(obj, str)


def get_img_srcs(html_text: str, selector: Optional[str]=None) -> list[str]:
    soup = BeautifulSoup(html_text, 'html.parser')
    new_selector = f'{selector} img' if selector is not None else 'img'
    imgs = soup.select(new_selector)
    paths = [img.get('src') for img in imgs]
    return [path for path in paths if is_attr_str(path)]
