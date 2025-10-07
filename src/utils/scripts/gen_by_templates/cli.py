import posixpath
from pathlib import Path

import typer
from inflection import camelize, underscore

app = typer.Typer(help="Plyaska Backend CLI - Generate files by templates")


def generate_by_template(template_folder: str, name: str, _type: str):
    if _type == "models":
        to_write = f"./src/{_type}/{name}.py"
    elif _type == "controllers":
        to_write = f"./src/{_type}/{name}_crud.py"
    elif _type == "tests":
        to_write = f"./tests/controllers/test_{name}s.py"
    else:
        to_write = f"./src/{_type}/{name}.py"
    with open(f"{template_folder}/{_type}.txt", "rt") as f:
        text = f.read().format(name=name, class_name=camelize(name))
        Path(to_write).write_text(text)
        typer.echo(f"🧱 Created a file of type {_type} in {to_write}")


@app.command()
def generate(name: str):
    """Сгенерировать заготовку файла с кодом.
    :param name: Писать в snake case
    """
    templates_folder_path = f"{posixpath.dirname(__file__)}/templates"

    file_name = underscore(name)

    types = [
        "models",
        "repositories",
        "services",
        "controllers",
        "tests",
    ]

    for value in types:
        generate_by_template(templates_folder_path, file_name, value)


if __name__ == "__main__":
    app()
