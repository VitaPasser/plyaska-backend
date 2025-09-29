from camelsnake import camel_to_snake  # type: ignore
import inflect


def pluralize_snake(name: str) -> str:
    parts = name.split("_")
    parts[-1] = inflect.engine().plural(text=parts[-1])
    return "_".join(parts)


def camel_to_db_name(name: str) -> str:
    return pluralize_snake(camel_to_snake(name))
