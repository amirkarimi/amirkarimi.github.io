from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import yaml
from yaml import Loader

DATA_FILE = 'data.yaml'

@dataclass
class NavItem:
    title: str
    link: str
    target: str | None = None


@dataclass
class Config:
    data: dict[str, Any]
    develop_mode: bool = False
    package_name: str = 'content'
    output_path: str = 'docs'
    domain: str = 'amirkarimi.dev'
    base_url: str = f'https://{domain}'
    year: int = datetime.now().year
    menu: list[NavItem] = field(default_factory=lambda :[
        NavItem('About', '/about'),
        NavItem('Blog', '/blog')
    ])

def load_config():
    with open(DATA_FILE, 'r') as f:
        data = yaml.load(f, Loader=Loader)
        config = Config(data)
        return config
