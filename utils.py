from pathlib import Path


def read_file(input_file_path: str) -> str:
    with open(input_file_path, 'r') as in_file:
        return in_file.read()


def write_file(output_file_path: str, content: str):
    with open(output_file_path, 'w') as out_file:
        out_file.write(content)


def truncate_title(title):
    return (title[:50] + '...') if len(title) > 50 else title
