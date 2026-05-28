from pydantic import BaseModel

class OutlineLoginData(BaseModel):
    out_url: str
    out_cert: str

class OutlineCreateKey(BaseModel):
    user_id: int

class OutlineCreateKeyReturn(BaseModel):
    key_name: str
    server_key_id: int
    access_url: str