from uuid import UUID

from fastapi import Request
from fastapi.datastructures import State


class AuthedState(State):
    user_id: UUID | None = None
    pass


class AuthedRequest(Request):
    state: AuthedState
    pass
