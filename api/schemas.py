"""Shared API response envelope: every endpoint returns { data, error, trace_id }."""

from typing import Generic, TypeVar

from pydantic import BaseModel

DataT = TypeVar("DataT")


class ErrorDetail(BaseModel):
    code: str
    message: str


class Envelope(BaseModel, Generic[DataT]):
    """Generic response envelope. Parametrize per endpoint, e.g. Envelope[HealthData]."""

    data: DataT | None = None
    error: ErrorDetail | None = None
    trace_id: str


class HealthData(BaseModel):
    status: str
    version: str
