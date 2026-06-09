from pydantic import BaseModel
from pydantic.functional_validators import BeforeValidator
from typing import Annotated

server_key_id = Annotated[str, BeforeValidator(lambda v: str(v) if v is not None else v)]

class OutlineLoginData(BaseModel):
    out_url: str
    out_cert: str

class OutlineCreateKey(BaseModel):
    user_id: int

class OutlineCreateKeyReturn(BaseModel):
    key_name: str
    server_key_id: server_key_id
    access_url: str