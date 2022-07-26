from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt


def datetime_serializer(value: datetime):
    return value.strftime("%d.%m.%Y %H:%M")


def datetime_serializer_timestamp(value: datetime):
    return value.timestamp()


class OnlyId(BaseModel):
    id: PositiveInt
