from pydantic import BaseModel

class VlessClientInit(BaseModel):
    ux_username: str
    ux_pass: str
    ux_url: str
    vless_inbound: int

class LoginData(BaseModel):
    username: str
    password: str