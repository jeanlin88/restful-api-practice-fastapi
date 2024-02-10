from typing import Any

from pydantic import BaseModel


class ResponseSuccess(BaseModel):
    success: bool = True
    result: Any
    pass


class ResponseFail(BaseModel):
    success: bool = False
    result: None = None
    error: str
    pass


def get_error_responses_dict(*status_codes: int) -> dict[int, dict]:
    value = {"model": ResponseFail}
    return {
        status_code: value
        for status_code in status_codes
    }
