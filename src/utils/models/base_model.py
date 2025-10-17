from typing import Dict, Any

from bson import Decimal128
from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    class Config:
        json_encoders = {
            Decimal128: lambda v: str(v.to_decimal()),
        }

    def update_from(self, other: PydanticBaseModel):
        """
        Recursively updates self with fields from another Pydantic model,
        using exclude_unset=True to avoid overwriting unset fields.
        """
        base_dict = self.model_dump()
        update_dict = other.model_dump(exclude_unset=True)

        def merge(d: Dict[str, Any], u: Dict[str, Any]):
            for k, v in u.items():
                if isinstance(v, dict) and isinstance(d.get(k), dict):
                    merge(d[k], v)
                else:
                    d[k] = v

        merge(base_dict, update_dict)
        return self.model_copy(update=base_dict)
