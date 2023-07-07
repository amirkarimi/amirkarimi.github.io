from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from urllib.parse import urljoin

from config import Config


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


@dataclass
class SiteMapRecord:
    relative_path: str
    updated_at: datetime
    priority: float

    @property
    def lastmod(self):
        return self.updated_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    def loc(self, config: Config):
        if self.relative_path is None or self.relative_path == "":
            return config.base_url
        else:
            return urljoin(config.base_url, str(self.relative_path))


@dataclass
class SiteMapData:
    records: list[SiteMapRecord] = field(default_factory=list)
