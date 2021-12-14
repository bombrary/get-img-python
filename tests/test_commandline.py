from commandline import extract_filename, make_path, rename_if_exists, download_imgs_from_urls
import pytest
from pytest import MonkeyPatch
from typing import Final
from requests.exceptions import HTTPError

test_cases_extract_filename: Final = [
    ("http://foo.com/img.png", "img.png"),
    ("http://foo.com/bar/img.png", "img.png"),
    ("http://foo.com/bar/img.png?q=123", "img.png"),
]

@pytest.mark.parametrize("url, expect", test_cases_extract_filename)
def test_extract_filename(url: str, expect: str):
    assert extract_filename(url) == expect


test_cases_make_path: Final = [
    ("http://foo.com/img.png", "imgout", "imgout/img.png"),
    ("http://foo.com/img.png", "imgout/", "imgout/img.png"),
    ("http://foo.com/bar/fuga/img.png", "imgout", "imgout/img.png"),
]

@pytest.mark.parametrize("url, output_dir, expect", test_cases_make_path)
def test_make_path(url: str, output_dir: str, expect: str):
    assert make_path(url, output_dir) == expect


test_cases_rename_if_exists: Final = [
    (["output/img.png"], "output/img.png", "output/img_1.png"),
    (["output/img.png", "output/img_1.png"], "output/img.png", "output/img_2.png"),
    (["output/img_1.png"], "output/img.png", "output/img.png"),
    (["output/img_1.png"], "output/img_1.png", "output/img_1_1.png"),
    (["output/img.png", "output/img_2.png"], "output/img.png", "output/img_1.png"),
]

@pytest.mark.parametrize("paths_exist, target, expect", test_cases_rename_if_exists)
def test_rename_if_exists(paths_exist: list[str], target: str, expect: str, monkeypatch: MonkeyPatch):
    def fake_exists(path: str):
        return path in paths_exist

    monkeypatch.setattr('os.path.exists', fake_exists)

    assert rename_if_exists(target) == expect


def test_download_imgs_from_urls(monkeypatch: MonkeyPatch):
    def fake_save_img(*_):
        pass

    class Response:
        def __init__(self):
            self.content = b'succeed'

    def fake_get(url: str) -> Response:
        if url == 'fail':
            raise HTTPError
        else:
            return Response()

    monkeypatch.setattr('commandline.save_img', fake_save_img)
    monkeypatch.setattr('requests.get', fake_get)

    urls = ["fail", "success", "fail", "fail"]
    failInfo = download_imgs_from_urls(urls, '.')
    assert len(failInfo) == 3


def test_download_imgs_from_urls_data_url(monkeypatch: MonkeyPatch):
    def fake_save_img(*_):
        pass

    monkeypatch.setattr('commandline.save_img', fake_save_img)

    url = "data:image/png;base64,BINIMAGE"
    failInfo = download_imgs_from_urls([url], '.')
    assert len(failInfo) == 0
