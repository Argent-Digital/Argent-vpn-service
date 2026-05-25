from pydantic import BaseModel, ConfigDict
from typing import List
from uuid import UUID

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