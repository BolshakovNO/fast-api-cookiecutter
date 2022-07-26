from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class Example(BaseModel):
    value: str
    children: list[str]


class ExampleWithChildren(BaseModel):
    value: str
    child_value: str


class CreateExample(BaseModel):
    value: str
    children: list[str]


class ExampleParent(BaseModel):
    value: str
