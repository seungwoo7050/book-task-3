"""
Web Proxy unit test.

실행 중인 server 없이 URL parsing과 cache key 로직을 직접 검증한다.

Usage:
    python3 -m pytest test_web_proxy.py -v
"""

import sys
import os

# import를 위해 `src/` directory를 path에 추가한다.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from web_proxy import parse_url, get_cache_path


class TestURLParsing:
    """URL parsing 동작을 검증한다."""

    def test_basic_url(self):
        host, port, path = parse_url("http://www.example.com/index.html")
        assert host == "www.example.com"
        assert port == 80
        assert path == "/index.html"

    def test_url_with_port(self):
        host, port, path = parse_url("http://www.example.com:8080/page")
        assert host == "www.example.com"
        assert port == 8080
        assert path == "/page"

    def test_url_no_path(self):
        host, port, path = parse_url("http://www.example.com")
        assert host == "www.example.com"
        assert port == 80
        assert path == "/"

    def test_url_with_trailing_slash(self):
        host, port, path = parse_url("http://www.example.com/")
        assert host == "www.example.com"
        assert port == 80
        assert path == "/"

    def test_url_with_query_string(self):
        host, port, path = parse_url("http://example.com/search?q=test")
        assert host == "example.com"
        assert port == 80
        assert path == "/search?q=test"

    def test_deep_path(self):
        host, port, path = parse_url("http://example.com/a/b/c/d.html")
        assert host == "example.com"
        assert path == "/a/b/c/d.html"


class TestCachePath:
    """cache key 생성 규칙을 검증한다."""

    def test_same_url_same_key(self):
        p1 = get_cache_path("http://example.com/a")
        p2 = get_cache_path("http://example.com/a")
        assert p1 == p2

    def test_different_url_different_key(self):
        p1 = get_cache_path("http://example.com/a")
        p2 = get_cache_path("http://example.com/b")
        assert p1 != p2
