from typing import Type

from markupsafe import Markup
from config import load_config
from jinja2 import Environment, PackageLoader, TemplateError, select_autoescape
from rich.console import Console
from markdown_parser import build_markdown
from processors import *
from watch import watch_files
from server import base_url, serve_forever
from utils import *
import requests
import sass
import typer
import xml.etree.ElementTree as ET


config = load_config()
console = Console()
app = typer.Typer()
env = Environment(
    loader=PackageLoader(config.package_name),
    autoescape=select_autoescape()
)
md = build_markdown()
env.filters['markdown'] = lambda text: Markup(md.convert(text))

processors: list[Type[Processor]] = [
    HomePage,
    PdfResume,
    CustomPages,
    Blog,
    Assets,
    Downloads,
    CName,
    SiteMap # Has to be the last one
]


def reset_output():
    shutil.rmtree(config.output_path, ignore_errors=True)
    Path(config.output_path).mkdir(exist_ok=True)


def build_all(develop_mode: bool):
    config.develop_mode = develop_mode
    print('Compiling...', end='')

    reset_output()

    sitemap_data = SiteMapData()
    
    try:
        for processor_class in processors:
            processor_class(env, config).run(sitemap_data)
        print(' [Done]')
    except (TemplateError, sass.CompileError):
        console.print_exception(show_locals=True)


def on_change(event):
    global config
    config = load_config()
    build_all(develop_mode=True)


@app.command()
def build():
    build_all(develop_mode=False)


@app.command()
def serve(watch: bool = typer.Option(False, help="Watch for changes."), addr: str = "localhost", port: int = 8000):
    config.base_url = base_url(addr, port)

    on_change(None)

    observer = None
    if watch:
        print("Monitoring for changes...")
        observer = watch_files(
            on_change,
            ignore_regexes=[r'\./.+\.py', r'\./docs(/.+)?'],
            ignore_directories=True
        )

    try:
        if observer:
            observer.start()
        serve_forever(addr, port, config)
    except KeyboardInterrupt:
        if observer:
            observer.stop()
            observer.join()


@app.command()
def test_sitemap():
    build()

    tree = ET.parse('docs/sitemap.xml')
    root = tree.getroot()
    for url_element in root:
        loc = url_element.findtext('./{*}loc')
        lastmod = url_element.findtext('./{*}lastmod')
        resp = requests.get(loc)
        print(loc, end=' ')
        status_ok = resp.status_code == 200
        content_ok = '<title>Amir Karimi' in str(resp.content) or loc.endswith('.pdf')
        if status_ok and content_ok:
            console.print('[OK]', style='green')
        else:
            console.print('[ERROR]', end=' ', style='red')
            if not status_ok:
                print(f'status: {resp.status_code}')
            else:
                print(f'content: {resp.content[:100]}...')

if __name__ == "__main__":
    app()
