from datetime import date, datetime
from models import MarkdownPage
import yaml
import markdown

SUMMARY_SEPARATOR = "<!--more-->"

def build_markdown():
    return markdown.Markdown(extensions=[
        'toc', 'fenced_code', 'tables', 'attr_list', 'codehilite', 'md_in_html'
    ])

def parse_date(val):
    if not val:
        return None
    if isinstance(val, datetime) or isinstance(val, date):
        return val
    return datetime.strptime(val, '%Y-%m-%d')


def parse_metadata(content: str) -> tuple[dict, str]:
    if not content.startswith('---'):
        return {}, content  # No metadata
    metadata_end_marker = content.find('---', 3)
    if metadata_end_marker == -1:
        return {}, content  # Invalid metadata marker
    metadata = yaml.safe_load(content[3:metadata_end_marker])
    return metadata, content[metadata_end_marker+4:]


def parse_markdown(markdown_content: str) -> MarkdownPage:
    metadata, markdown_content = parse_metadata(markdown_content)
    md = build_markdown()
    html_content = md.convert(markdown_content)

    summary_separator_index = html_content.find(SUMMARY_SEPARATOR)

    return MarkdownPage(
        template=metadata.get('template', 'page.html'),
        content=html_content,
        summary=html_content if summary_separator_index == -
        1 else html_content[:summary_separator_index],
        title=metadata.get('title'),
        date=parse_date(metadata.get('date')),
        keywords=metadata.get('keywords'),
        slug=metadata.get('slug'),
        toc=md.toc_tokens, # type: ignore
        category=metadata.get('category'),
        hide_toc=metadata.get('hide_toc', False)
    )
