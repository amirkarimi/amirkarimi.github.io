import shutil
from pathlib import Path
from config import OUTPUT_PATH


def read_file(input_file_path: str) -> str:
    with open(input_file_path, 'r') as in_file:
        return in_file.read()


def write_file(output_file_path: str, content: str):
    with open(output_file_path, 'w') as out_file:
        out_file.write(content)


def make_out_dir():
    Path(OUTPUT_PATH).mkdir(exist_ok=True)


def clean_out_dir():
    shutil.rmtree(OUTPUT_PATH, ignore_errors=True)


def truncate_title(title):
    return (title[:50] + '...') if len(title) > 50 else title
