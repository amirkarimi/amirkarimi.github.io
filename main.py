from config import config, PACKAGE_NAME, OUTPUT_PATH
from jinja2 import Environment, PackageLoader, TemplateError, select_autoescape
from pathlib import Path
from rich.console import Console
from markdown_parser import parse_markdown
from models import LinkInfo, Navigation, Post
from watch import watch_files
from server import base_url, serve_forever
from utils import *
import sass
import shutil
import typer


console = Console()
app = typer.Typer()
env = Environment(
    loader=PackageLoader(PACKAGE_NAME),
    autoescape=select_autoescape()
)

def render_home_page():
    template_file = 'index.html'
    template = env.get_template(template_file)
    write_file(f'{OUTPUT_PATH}/{template_file}',
               template.render(config=config))


def compile_assets():
    input_assets_path = Path(PACKAGE_NAME, 'assets')
    output_assets_path = Path(OUTPUT_PATH, 'assets')

    # Image
    shutil.copytree(input_assets_path.joinpath('img'),
                    output_assets_path.joinpath('img'))

    # CSS
    shutil.copytree(input_assets_path.joinpath('css'),
                    output_assets_path.joinpath('css'))

    # Scss
    sass_input_path = input_assets_path.joinpath('scss')
    sass_output_path = output_assets_path.joinpath('css')
    sass_output_path.mkdir(exist_ok=True)
    file_name = 'main'
    with open(sass_output_path.joinpath(f'{file_name}.css'), 'w') as css:
        css.write(sass.compile(filename=str(
            sass_input_path.joinpath(f'{file_name}.scss'))))

    # JS
    js_files = [
        'bootstrap/dist/js/bootstrap.min.js',
        '@popperjs/core/dist/umd/popper.min.js'
    ]
    js_output_path = output_assets_path.joinpath('js')
    js_output_path.mkdir(exist_ok=True)
    for js_file in js_files:
        js_file_path = Path('./node_modules').joinpath(js_file)
        shutil.copyfile(
            js_file_path, js_output_path.joinpath(js_file_path.name))


def collect_downloads():
    input_downloads_path = Path(PACKAGE_NAME, 'downloads')
    output_downloads_path = Path(OUTPUT_PATH, 'downloads')
    shutil.copytree(input_downloads_path, output_downloads_path)


def render_pages():
    for input_file in Path(PACKAGE_NAME, 'pages').iterdir():
        if input_file.is_file() and input_file.suffix == '.md':
            context = parse_markdown(read_file(input_file))
            template = env.get_template(context.template)
            output_content = template.render(page=context, config=config)

            page_output_dir = Path(f'{OUTPUT_PATH}/{input_file.stem}')
            page_output_dir.mkdir(exist_ok=True)
            write_file(page_output_dir.joinpath('index.html'), output_content)


def render_blog():
    posts: list[Post] = []
    prev_post = None
    input_files = sorted(Path(PACKAGE_NAME, 'blog').iterdir(), reverse=True)
    for input_file in input_files:
        if input_file.is_file() and input_file.suffix == '.md':
            markdown_page = parse_markdown(read_file(input_file))
            post = Post(
                markdown_page=markdown_page,
                navigation=Navigation(
                    f'blog/{markdown_page.date.strftime("%Y/%m/%d")}/{markdown_page.slug}')
            )
            posts.append(post)
            if prev_post:
                prev_post.navigation.older_link = LinkInfo(
                    post.navigation.url, truncate_title(post.markdown_page.title))
                post.navigation.newer_link = LinkInfo(
                    prev_post.navigation.url, truncate_title(prev_post.markdown_page.title))
            prev_post = post

    redirect_template = env.get_template('redirect.html')

    # Render post pages
    for post in posts:
        if not post.markdown_page.slug:
            raise RuntimeError(f'slug metadata is not set for {input_file}.')

        template = env.get_template(post.markdown_page.template)
        output_content = template.render(
            page=post.as_view_context,
            config=config)

        page_output_dir = Path(OUTPUT_PATH, post.navigation.path)
        page_output_dir.mkdir(parents=True, exist_ok=True)
        write_file(page_output_dir.joinpath('index.html'), output_content)

        # Backward compatible URL redirection
        redirect_output_dir = Path(
            OUTPUT_PATH, post.navigation.path.lstrip('blog/').rstrip(post.markdown_page.slug))
        redirect_output_dir.mkdir(parents=True, exist_ok=True)
        redirect_output_file_path = redirect_output_dir.joinpath(f'{post.markdown_page.slug}.html')
        write_file(redirect_output_file_path,
                   redirect_template.render(url=post.navigation.url))

    # Render blog index
    template = env.get_template('blog.html')
    blog_index_page_path = Path(OUTPUT_PATH, 'blog/index.html')
    blog_index_content = template.render(
        posts=(p.as_view_context for p in posts),
        config=config)
    write_file(blog_index_page_path, blog_index_content)


def set_cname():
    write_file(Path(OUTPUT_PATH, 'CNAME'), config.domain)


def build_all(develop_mode: bool):
    config.develop_mode = develop_mode
    print('Compiling...', end='')

    clean_out_dir()
    make_out_dir()
    try:
        render_home_page()
        render_pages()
        render_blog()
        compile_assets()
        collect_downloads()
        set_cname()
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
            ignore_regexes=[r'\./.+\.py', r'\./out(/.+)?'],
            ignore_directories=True
        )

    try:
        if observer:
            observer.start()
        serve_forever(addr, port)
    except KeyboardInterrupt:
        if observer:
            observer.stop()
            observer.join()


if __name__ == "__main__":
    app()
