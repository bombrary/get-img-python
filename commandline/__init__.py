from getimg import get_img_urls
from typing import Optional
import requests
from requests.exceptions import RequestException
import urllib.parse
import os.path
from tqdm import tqdm
import w3lib.url


def print_log(text: str, need_log: bool):
    if need_log:
        print(text)


FailInfo = tuple[str, RequestException | ValueError]


def download_imgs_from_page(url: str, output_dir: str, selector: Optional[str]=None, need_log: bool=False) -> list[FailInfo]:
    urls = get_img_urls(url, selector)
    return download_imgs_from_urls(urls, output_dir, need_log)


def download_imgs_from_urls(urls: list[str], output_dir: str, need_log: bool=False) -> list[FailInfo]:
    failInfo = []
    urls_with_pbar = tqdm(urls) if need_log else urls
    for url in urls_with_pbar:
        if is_dataurl(url):
            e = save_img_from_data_url(url, output_dir, need_log)
            if e is not None:
                failInfo.append((url[0:100] + '...', e))
        else:
            e = download_img_from_url(url, output_dir, need_log)
            if e is not None:
                failInfo.append((url, e))
    return failInfo


def is_dataurl(url: str) -> bool:
    return url.startswith('data:')


def parse_ext_from_mime(mime: str) -> str:
    [_, type] = mime.split('/')
    if type == 'svg+xml':
        return 'svg'
    else:
        return type


def save_img_from_data_url(url: str, output_dir: str, need_log: bool=False) -> Optional[ValueError]:
    try:
        result = w3lib.url.parse_data_uri(url)
    except ValueError as e:
        return e

    ext = parse_ext_from_mime(result.media_type)

    path = f'{output_dir}/dara_url.{ext}'
    save_img(path, result.data)

    print_log(f'(Data URL) -> {path}', need_log)


def download_img_from_url(url: str, output_dir: str, need_log: bool=False) -> Optional[RequestException]:
    path = make_path(url, output_dir)
    try:
        res = requests.get(url)
    except RequestException as e:
        return e

    save_img(path, res.content)

    print_log(f'{url} -> {path}', need_log)


def extract_filename(url: str) -> str:
    urlinfo = urllib.parse.urlparse(url)
    return os.path.basename(urlinfo.path)


def make_path(url: str, output_dir: str) -> str:
    output_dir = output_dir.rstrip('/')
    path = f'{output_dir}/{extract_filename(url)}'
    return path


def save_img(path: str, content: bytes):
    path = rename_if_exists(path)
    with open(path, 'wb') as f:
        f.write(content)


def rename_if_exists(path) -> str:
    if not os.path.exists(path):
        return path
    else:
        root, ext = os.path.splitext(path)
        i = 1
        while True:
            new_path = f'{root}_{i}{ext}'
            if not os.path.exists(new_path):
                return new_path
            i += 1
