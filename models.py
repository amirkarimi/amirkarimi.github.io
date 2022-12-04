from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass
class MarkdownPage():
    template: str
    content: str
    summary: str
    title: str | None
    date: datetime
    keywords: str | None
    slug: str | None
    toc: list
    category: str | None
    hide_toc: bool


@dataclass
class LinkInfo:
    url: str
    title: str


@dataclass
class Navigation:
    path: str
    older_link: LinkInfo | None = None
    newer_link: LinkInfo | None = None

    @property
    def url(self):
        return f'/{self.path}'


@dataclass
class Post:
    markdown_page: MarkdownPage
    navigation: Navigation

    @property
    def as_view_context(self):
        d = asdict(self.markdown_page)
        d.update(asdict(self.navigation))
        d['url'] = self.navigation.url
        return d
