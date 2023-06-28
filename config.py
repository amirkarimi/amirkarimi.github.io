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
    domain: str = 'amirkarimi.dev'
    base_url: str = f'https://{domain}'
    name: str = 'Amir Karimi'
    title: str = 'Fractional VP of Engineering'
    year: int = datetime.now().year
    menu: list[NavItem] = field(default_factory=lambda :[
        NavItem('About', '/about'),
        NavItem('Blog', '/blog'),
        NavItem('Contact', 'mailto:info@amirkarimi.dev', target='_blank'),
    ])
