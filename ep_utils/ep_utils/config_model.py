import os
import re

from pydantic import BaseModel


class ConfigModel(BaseModel):
    def __init__(self) -> None:
        class_name = self._camelcase_to_snakecase(self.__class__.__name__)
        data = dict()
        for key, field in self.__fields__.items():
            data[key] = field.type_(
                os.environ.get(f"{class_name}__{key.upper()}", field.default)
            )
        super().__init__(**data)

    @staticmethod
    def _camelcase_to_snakecase(string):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", string).upper()

    @classmethod
    def get_fields_defaults(cls):
        class_name = cls._camelcase_to_snakecase(cls.__name__)
        return {
            f"{class_name}__{key.upper()}": os.environ.get(
                f"{class_name}__{key.upper()}"
            ) or str(field.default or "")
            for key, field in cls.__fields__.items()
        }
