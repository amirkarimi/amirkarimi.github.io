from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class NavItem:
    title: str
    link: str
    target: str | None = None


@dataclass
class Config:
    develop_mode: bool = False
    package_name: str = 'content'
    output_path: str = 'docs'
    domain: str = 'www.4m1r.dev'
    base_url: str = f'https://{domain}'
    name: str = 'Amir Karimi'
    title: str = 'Software Engineer'
    year: int = datetime.now().year
    menu: list[NavItem] = field(default_factory=lambda :[
        NavItem('About', '/about'),
        NavItem('Blog', '/blog'),
        NavItem('Contact', 'mailto:hey@4m1r.dev', target='_blank'),
    ])