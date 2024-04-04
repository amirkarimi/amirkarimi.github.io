from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
import yaml
from yaml import Loader

DATA_FILE = "data.yaml"


@dataclass
class NavItem:
    title: str
    link: str
    target: str | None = None


@dataclass
class Config:
    data: dict[str, Any]
    develop_mode: bool = False
    package_name: str = "content"
    output_path: str = "docs"
    domain: str = "amirkarimi.dev"
    base_url: str = f"https://{domain}"
    year: int = datetime.now().year
    now: datetime = datetime.now()
    menu: list[NavItem] = field(
        default_factory=lambda: [
            NavItem("Blog", "/blog/"),
            NavItem("About", "/about/"),
        ]
    )

    @property
    def domain_with_www(self):
        return "www." + self.domain

    @property
    def pdf_resume_path(self):
        return f"/downloads/amirkarimi-resume-{self.now.date().isoformat()}.pdf"


def load_config():
    with open(DATA_FILE, "r") as f:
        data = yaml.load(f, Loader=Loader)
        config = Config(data)
        return config
