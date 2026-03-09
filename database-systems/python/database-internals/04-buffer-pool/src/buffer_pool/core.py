from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory


@dataclass(slots=True)
class Entry:
    key: str
    value: object


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._items: OrderedDict[str, object] = OrderedDict()

    def get(self, key: str) -> object | None:
        if key not in self._items:
            return None
        self._items.move_to_end(key, last=False)
        return self._items[key]

    def put(self, key: str, value: object) -> Entry | None:
        if key in self._items:
            self._items[key] = value
            self._items.move_to_end(key, last=False)
            return None
        evicted = None
        if len(self._items) >= self.capacity:
            old_key, old_value = self._items.popitem(last=True)
            evicted = Entry(old_key, old_value)
        self._items[key] = value
        self._items.move_to_end(key, last=False)
        return evicted

    def delete(self, key: str) -> bool:
        return self._items.pop(key, None) is not None

    def has(self, key: str) -> bool:
        return key in self._items

    def keys(self) -> list[str]:
        return list(self._items.keys())

    def size(self) -> int:
        return len(self._items)


@dataclass(slots=True)
class Page:
    page_id: str
    data: bytearray
    dirty: bool = False
    pin_count: int = 0


class BufferPool:
    def __init__(self, max_pages: int, page_size: int = 4096) -> None:
        self.max_pages = max_pages
        self.page_size = page_size or 4096
        self.cache = LRUCache(max_pages)
        self.file_handles: dict[str, object] = {}

    def fetch_page(self, page_id: str) -> Page:
        cached = self.cache.get(page_id)
        if cached is not None:
            page = cached
            assert isinstance(page, Page)
            page.pin_count += 1
            return page

        file_path, page_number = parse_page_id(page_id)
        handle = self._get_handle(file_path)
        handle.seek(page_number * self.page_size)
        data = bytearray(handle.read(self.page_size))
        page = Page(page_id, data, pin_count=1)

        evicted = self.cache.put(page_id, page)
        if evicted is not None:
            evicted_page = evicted.value
            assert isinstance(evicted_page, Page)
            if evicted_page.pin_count > 0:
                self.cache.put(evicted.key, evicted_page)
                raise RuntimeError("bufferpool: cannot evict pinned page")
            if evicted_page.dirty:
                self._write_page(evicted_page)
        return page

    def unpin_page(self, page_id: str, is_dirty: bool) -> None:
        cached = self.cache.get(page_id)
        if cached is None:
            return
        page = cached
        assert isinstance(page, Page)
        if page.pin_count > 0:
            page.pin_count -= 1
        if is_dirty:
            page.dirty = True

    def flush_page(self, page_id: str) -> None:
        cached = self.cache.get(page_id)
        if cached is None:
            return
        page = cached
        assert isinstance(page, Page)
        if not page.dirty:
            return
        self._write_page(page)
        page.dirty = False

    def flush_all(self) -> None:
        for key in self.cache.keys():
            self.flush_page(key)

    def close(self) -> None:
        self.flush_all()
        for handle in self.file_handles.values():
            handle.close()
        self.file_handles.clear()

    def _get_handle(self, file_path: str):
        handle = self.file_handles.get(file_path)
        if handle is None:
            handle = Path(file_path).open("r+b")
            self.file_handles[file_path] = handle
        return handle

    def _write_page(self, page: Page) -> None:
        file_path, page_number = parse_page_id(page.page_id)
        handle = self._get_handle(file_path)
        handle.seek(page_number * self.page_size)
        handle.write(page.data)
        handle.flush()


def parse_page_id(page_id: str) -> tuple[str, int]:
    if ":" not in page_id:
        raise ValueError("bufferpool: invalid page id")
    file_path, page_number = page_id.rsplit(":", 1)
    return str(Path(file_path)), int(page_number)


def demo() -> None:
    with TemporaryDirectory(prefix="buffer-pool-") as temp_dir:
        data_file = Path(temp_dir) / "data.db"
        pages = bytearray()
        for index in range(4):
            page = bytearray(64)
            payload = f"page-{index}".encode()
            page[: len(payload)] = payload
            pages.extend(page)
        data_file.write_bytes(pages)
        pool = BufferPool(2, 64)
        page = pool.fetch_page(f"{data_file}:0")
        print({"page_id": page.page_id, "pin_count": page.pin_count, "prefix": page.data[:6].decode()})
