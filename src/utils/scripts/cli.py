import posixpath
from pathlib import Path

import inflect
import typer
from camelsnake import snake_to_camel  # type: ignore

app = typer.Typer(help="Plyaska Backend CLI")


def generate_by_template(template_folder: str, name: str, _type: str):
    if _type == "models":
        to_write = f"./src/{_type}/{name}.py"
    else:
        to_write = f"./src/{_type}/{name}{snake_to_camel(inflect.engine().singular_noun(text=_type)).capitalize()}.py"
    with open(f"{template_folder}/{_type}.txt", "rt") as f:
        Path(to_write).write_text(f.read().format(name=name))
        typer.echo(f"Создан файл типа {_type} {to_write}")


@app.command()
def generate(name: str):
    """Сгенерировать заготовку файла с кодом.
    :param name: Писать в snake case
    """
    templates_folder_path = f"{posixpath.dirname(__file__)}/templates"

    camel_name = snake_to_camel(name).capitalize()

    types = [
        "models",
        "repositories",
        "services",
        "controllers",
    ]

    for value in types:
        generate_by_template(templates_folder_path, camel_name, value)


if __name__ == "__main__":
    app()
