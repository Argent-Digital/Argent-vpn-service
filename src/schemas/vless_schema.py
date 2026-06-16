from pydantic import BaseModel, Field, model_serializer, ConfigDict
import json
from uuid import UUID
from typing import List


class VlessClientInit(BaseModel):
    ux_username: str
    ux_pass: str
    ux_url: str
    vless_inbound: int
    port: int
    ip: str
    path: str | None = None
    reality_public_key: str
    reality_short_id: str

class LoginData(BaseModel):
    username: str
    password: str

class KeyData(BaseModel):
    user_id: int

class AddKeyReturn(BaseModel):
     key_name: str
     access_url: str
     vless_uuid: UUID

class KeyDelData(BaseModel):
    vless_uuid: UUID

class ClientData(BaseModel):
        id: str
        alterId: int = 0
        email: str
        limitIp: int = 10
        totalGB: int = 0
        expiryTime: int = 0
        enable: bool = True
        tgId: int
        subId: str = ""

class InboundSettingsWrap(BaseModel):
    clients: list[ClientData]

class AddClientPayload(BaseModel):
    id: int
    settings: InboundSettingsWrap

    @model_serializer
    def serialize_for_panel(self) -> dict:
        return {
            "id": self.id,
            "settings": json.dumps(self.settings.model_dump()),
        }
    
