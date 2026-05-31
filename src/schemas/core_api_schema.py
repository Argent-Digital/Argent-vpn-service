from pydantic import BaseModel, ConfigDict
from uuid import UUID
from src.schemas.billing_schema import NodeData

class VpnReturnData(BaseModel):
    server_key_id: str | None
    key_name: str
    access_url: str
    vless_uuid: UUID | None

class CreateKey(BaseModel):
    user_id: int
    protocol: str

    model_config = ConfigDict(from_attributes=True)

class CreateKeyClientBody(BaseModel):
    node_data: NodeData
    user_data: CreateKey

class DeleteKeys(BaseModel):
    user_id: int
    node_id: int
    server_key_id: str| None = None
    protocol: str
    vless_uuid: UUID | None = None

    model_config=ConfigDict(from_attributes=True)

class DelKeyData(BaseModel):
    node_data: NodeData
    key_data: DeleteKeys
