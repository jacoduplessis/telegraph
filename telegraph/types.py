from typing import NamedTuple, List


class Account(NamedTuple):
    short_name: str = ''
    author_name: str = ''
    author_url: str = ''
    access_token: str = None
    auth_url: str = None
    page_count: int = None


class Page(NamedTuple):
    path: str
    url: str
    title: str
    description: str
    views: int
    author_name: str = None
    author_url: str = None
    image_url: str = None
    content: List = None
    can_edit: bool = None


class PageViews(NamedTuple):
    views: int


class PageList(NamedTuple):
    total_count: int
    pages: List[Page]