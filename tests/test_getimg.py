from getimg import get_img_srcs, get_img_urls
from typing import Final
from pytest import MonkeyPatch

html_text: Final = """
<html>
    <body>
        <div class="container1">
            <img src="http://loc1.com/foo/img1.png">
            <img src="/img2.png">
        </div>
        <div class="container2">
            <img src="../img3.png">
            <img src="//loc2.com/img4.png">
            <img src="data:image/png;base64,BINIMAGE">
        </div>
    </body>
</html>
"""

def test_get_src():
    expect = [
        "http://loc1.com/foo/img1.png",
        "/img2.png",
        "../img3.png",
        "//loc2.com/img4.png",
        "data:image/png;base64,BINIMAGE"
    ]

    assert get_img_srcs(html_text) == expect


class Result:
    def __init__(self, url: str):
        self.text = html_text
        self.url = url

def fake_get(url: str) -> Result:
    return Result(url)


def test_get_url(monkeypatch: MonkeyPatch):
    monkeypatch.setattr('requests.get', fake_get)


    url = "http://loc.com/foo/"
    expect = [
        "http://loc1.com/foo/img1.png",
        "http://loc.com/img2.png",
        "http://loc.com/img3.png",
        "http://loc2.com/img4.png",
        "data:image/png;base64,BINIMAGE"
    ]

    assert get_img_urls(url) == expect


def test_get_url_with_selector(monkeypatch: MonkeyPatch):
    monkeypatch.setattr('requests.get', fake_get)

    url = "http://loc.com/foo/"
    expect = [
        "http://loc.com/img3.png",
        "http://loc2.com/img4.png",
        "data:image/png;base64,BINIMAGE"
    ]

    assert get_img_urls(url, ".container2") == expect
