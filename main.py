from typing import Type
from config import Config
from jinja2 import Environment, PackageLoader, TemplateError, select_autoescape
from rich.console import Console
from processors import *
from watch import watch_files
from server import base_url, serve_forever
from utils import *
import sass
import typer


config = Config()
console = Console()
app = typer.Typer()
env = Environment(
    loader=PackageLoader(config.package_name),
    autoescape=select_autoescape()
)

processors: list[Type[Processor]] = [
    HomePage,
    CustomPages,
    Blog,
    Assets,
    Downloads,
    CName
]


def reset_output():
    shutil.rmtree(config.output_path, ignore_errors=True)
    Path(config.output_path).mkdir(exist_ok=True)


def build_all(develop_mode: bool):
    config.develop_mode = develop_mode
    print('Compiling...', end='')

    reset_output()
    try:
        for processor_class in processors:
            processor_class(env, config).run()
        print(' [Done]')
    except (TemplateError, sass.CompileError):
        console.print_exception(show_locals=True)


def on_change(event):
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


if __name__ == "__main__":
    app()
