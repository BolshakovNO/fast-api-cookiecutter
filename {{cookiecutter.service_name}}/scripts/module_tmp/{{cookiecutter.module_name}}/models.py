from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class {{cookiecutter.module_name | capitalize}}(BaseModel):
    value: str
