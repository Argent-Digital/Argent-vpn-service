from pydantic import BaseModel, Field, model_serializer, ConfigDict
import json
from uuid import UUID
from typing import List


class VlessClientInit(BaseModel):
    ux_username: str
    ux_pass: str
    ux_url: str
    vless_inbound: int
    ip: str
    path: str | None

class LoginData(BaseModel):
    username: str
    password: str

class KeyData(BaseModel):
    user_id: str

class KeyDelData(BaseModel):
    user_id: str
    vless_uuid: UUID

class ClientData(BaseModel):
        id: UUID
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

class NodeData(BaseModel):
    ip: str

    ux_username: str | None = None
    ux_pass: str | None = None
    ux_url: str | None = None
    vless_inbound: int | None = None

    out_url: str | None = None
    out_cert: str | None = None

    model_config = ConfigDict(from_attributes=True)

class DeleteKeys(BaseModel):
    user_id: int
    node_id: int
    server_key_id: str| None = None
    protocol: str
    vless_uuid: UUID | None = None

    model_config=ConfigDict(from_attributes=True)

class DelKeysData(BaseModel):
    nodes_list: List[NodeData]
    keys_list: List[DeleteKeys]