import logging
from typing import Any, get_args, get_origin, Optional

from beanie import Document, Link
from pydantic import BaseModel, create_model


def convert_type_recursively(tp: Any, visited: set[int], name_suffix: str):
    """
    Recursively converts the type:

    - Link [...] -> str
    - Basemodel -> Dynamically created a new model
    - support List, Dict, Optional, etc.
    """
    if id(tp) in visited:
        return tp
    visited.add(id(tp))

    # Link -> str
    if get_origin(tp) is Link:
        return str

    # Support for containers: list, dict, tuple, Optional/Union
    origin = get_origin(tp)
    if origin in (list, set, tuple):
        args = tuple(
            convert_type_recursively(a, visited, name_suffix) for a in get_args(tp)
        )
        return origin[args] # type: ignore
    if origin is dict:
        k, v = get_args(tp)
        return dict[convert_type_recursively(k, visited, name_suffix), convert_type_recursively(v, visited, name_suffix)] # type: ignore
    if origin is not None:  # Union / Annotated / etc.
        args = tuple(
            convert_type_recursively(a, visited, name_suffix) for a in get_args(tp)
        )
        return origin[args] # type: ignore

    # Inquired Pydantic model
    if isinstance(tp, type) and issubclass(tp, BaseModel):
        return make_input_schema(
            tp, name_suffix=name_suffix, exclude_fields=set(), _visited=visited
        )

    return tp


def make_input_schema(
    model: type[BaseModel],
    *,
    name_suffix: str = "Create",
    exclude_fields: set[str] | None = None,
    _visited: set[int] | None = None,
    update: bool = False,
) -> type[BaseModel]:
    """
    Creates a Pydantic scheme:

    - Link [...] -> str (including nested models)
    - Basemodel inside are also processed
    """
    visited = _visited or set()
    exclude_fields = exclude_fields or {
        "id",
        "revision_id",
        "_id",
        "created_at",
        "updated_at",
    }
    fields: dict[str, tuple[Any, Any]] = {}

    logging.debug(f"fields={model.model_fields}, items={model.model_fields.items()}")

    for fname, f in model.model_fields.items():
        if fname in exclude_fields:
            continue

        new_type = convert_type_recursively(f.annotation, visited, name_suffix)

        if update:
            new_type = Optional[new_type]
            default = None
        else:
            default = f.default if f.default is not None else ...

        fields[fname] = (new_type, default)

    return create_model(f"{model.__name__}{name_suffix}", **fields)


def make_create_schema(model: type[Document]):
    return make_input_schema(model=model, name_suffix="Create")


def make_update_schema(model: type[Document]):
    return make_input_schema(model=model, name_suffix="Update", update=True)
