import camelsnake
import inflect


def pluralize_snake(name: str) -> str:
    parts = name.split("_")
    parts[-1] = inflect.engine().plural(text=parts[-1])
    return "_".join(parts)

def camel_to_db_name(name: str) -> str:
    return pluralize_snake(camelsnake.camel_to_snake(name))