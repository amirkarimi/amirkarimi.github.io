from datetime import datetime, time
import shutil
from abc import ABC, abstractmethod
from pathlib import Path

import sass
from jinja2 import Environment

from config import Config
from markdown_parser import parse_markdown
from models import LinkInfo, Navigation, Post, SiteMapData, SiteMapRecord
from utils import *


class Processor(ABC):
    env: Environment
    config: Config

    def __init__(self, env: Environment, config: Config):
        self.env = env
        self.config = config

    @abstractmethod
    def run(self, sitemap: SiteMapData):
        pass


class HomePage(Processor):
    def run(self, sitemap: SiteMapData):
        template_file = "index.html"
        template = self.env.get_template(template_file)
        write_file(
            f"{self.config.output_path}/{template_file}",
            template.render(config=self.config),
        )

        # Add sitemap data
        sitemap.records.append(
            SiteMapRecord(
                relative_path="",
                updated_at=self.config.now
            )
        )


class PdfResume(Processor):
    def run(self, sitemap: SiteMapData):
        template_file = "pdf_resume.html"
        template = self.env.get_template(template_file)
        write_file(
            f"{self.config.output_path}/{template_file}",
            template.render(config=self.config),
        )


class CustomPages(Processor):
    def run(self, sitemap: SiteMapData):
        for input_file in Path(self.config.package_name, "pages").iterdir():
            if input_file.is_file() and input_file.suffix == ".md":
                context = parse_markdown(read_file(input_file))
                template = self.env.get_template(context.template)
                output_content = template.render(page=context, config=self.config)
                page_output_dir = Path(f"{self.config.output_path}/{input_file.stem}")
                page_output_dir.mkdir(exist_ok=True)
                write_file(page_output_dir.joinpath("index.html"), output_content)

                # Add sitemap data
                sitemap.records.append(
                    SiteMapRecord(
                        relative_path=add_trailing_slash(input_file.stem),
                        updated_at=datetime(context.date.year, context.date.month, context.date.day) if context.date else self.config.now
                    )
                )


class Blog(Processor):
    def run(self, sitemap: SiteMapData):
        last_update = None
        posts: list[Post] = []
        prev_post = None
        input_files = sorted(
            Path(self.config.package_name, "blog").iterdir(), reverse=True
        )
        for input_file in input_files:
            if input_file.is_file() and input_file.suffix == ".md":
                markdown_page = parse_markdown(read_file(input_file))
                post = Post(
                    markdown_page=markdown_page,
                    navigation=Navigation(
                        f'blog/{markdown_page.date.strftime("%Y/%m/%d")}/{markdown_page.slug}/'
                    ),
                )
                posts.append(post)
                if prev_post:
                    prev_post.navigation.older_link = LinkInfo(
                        post.navigation.url, truncate_title(post.markdown_page.title)
                    )
                    post.navigation.newer_link = LinkInfo(
                        prev_post.navigation.url,
                        truncate_title(prev_post.markdown_page.title),
                    )
                prev_post = post

        redirect_template = self.env.get_template("redirect.html")

        # Render post pages
        for post in posts:
            if not post.markdown_page.slug:
                raise RuntimeError(f"slug metadata is not set for {input_file}.")

            template = self.env.get_template(post.markdown_page.template)
            output_content = template.render(
                page=post.as_view_context, config=self.config
            )

            page_output_dir = Path(self.config.output_path, post.navigation.path)
            page_output_dir.mkdir(parents=True, exist_ok=True)
            write_file(page_output_dir.joinpath("index.html"), output_content)

            post_date = datetime.combine(post.markdown_page.date, time(0, 0))
            if not last_update or last_update < post_date:
                last_update = post_date
            # Add sitemap data
            sitemap.records.append(
                SiteMapRecord(
                    relative_path=post.navigation.path,
                    updated_at=post_date
                )
            )

            # Backward compatible URL redirection
            redirect_output_dir = Path(
                self.config.output_path,
                post.navigation.path.lstrip("blog/").rstrip(post.markdown_page.slug + "/"),
            )
            redirect_output_dir.mkdir(parents=True, exist_ok=True)
            redirect_output_file_path = redirect_output_dir.joinpath(
                f"{post.markdown_page.slug}.html"
            )
            write_file(
                redirect_output_file_path,
                redirect_template.render(url=post.navigation.url),
            )

        # Render blog index
        template = self.env.get_template("blog.html")
        blog_index_page_path = Path(self.config.output_path, "blog/index.html")
        blog_index_content = template.render(
            posts=(p.as_view_context for p in posts), config=self.config
        )
        write_file(blog_index_page_path, blog_index_content)

        # Blog root page
        sitemap.records.append(
            SiteMapRecord(
                relative_path="blog/",
                updated_at=last_update,
            )
        )


class Assets(Processor):
    def run(self, sitemap: SiteMapData):
        input_assets_path = Path(self.config.package_name, "assets")
        output_assets_path = Path(self.config.output_path, "assets")

        # Image
        shutil.copytree(
            input_assets_path.joinpath("img"), output_assets_path.joinpath("img")
        )

        # CSS
        shutil.copytree(
            input_assets_path.joinpath("css"), output_assets_path.joinpath("css")
        )

        # Scss
        sass_input_path = input_assets_path.joinpath("scss")
        sass_output_path = output_assets_path.joinpath("css")
        sass_output_path.mkdir(exist_ok=True)

        for file_path in sass_input_path.iterdir():
            with open(
                sass_output_path.joinpath(file_path.with_suffix(".css").name), "w"
            ) as css:
                css.write(sass.compile(filename=str(file_path)))

        # JS
        js_files = [
            "bootstrap/dist/js/bootstrap.min.js",
            "@popperjs/core/dist/umd/popper.min.js",
        ]
        js_output_path = output_assets_path.joinpath("js")
        js_output_path.mkdir(exist_ok=True)
        for js_file in js_files:
            js_file_path = Path("./node_modules").joinpath(js_file)
            shutil.copyfile(js_file_path, js_output_path.joinpath(js_file_path.name))


class Downloads(Processor):
    def run(self, sitemap: SiteMapData):
        input_downloads_path = Path(self.config.package_name, "downloads")
        output_downloads_path = Path(self.config.output_path, "downloads")
        shutil.copytree(input_downloads_path, output_downloads_path)

        for file in input_downloads_path.iterdir():
            if file.is_file():
                
                # Add sitemap data
                sitemap.records.append(
                    SiteMapRecord(
                        relative_path=Path("downloads").joinpath(file.name),
                        updated_at=datetime.fromtimestamp(file.lstat().st_mtime)
                    )
                )


class CName(Processor):
    def run(self, sitemap: SiteMapData):
        write_file(Path(self.config.output_path, "CNAME"), self.config.domain)


class SiteMap(Processor):
    def run(self, sitemap: SiteMapData):
        template_file = "sitemap.xml"
        template = self.env.get_template(template_file)
        write_file(
            f"{self.config.output_path}/{template_file}",
            template.render(sitemap=sitemap, config=self.config),
        )
