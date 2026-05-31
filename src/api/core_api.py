from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.dependencies import get_current_user_id
from src.schemas.core_api_schema import CreateKeyClientBody, DelKeyData, VpnReturnData
from src.schemas.vless_schema import VlessClientInit, KeyDelData, KeyData, AddKeyReturn
from src.schemas.outline_schema import OutlineLoginData, OutlineCreateKey
from src.client.vless_panel_client import VlessPanelClient
from src.client.outline_client import OutlinePanelClient

router = APIRouter(prefix="/vpn", tags=["core api"])

@router.post("/vpn/create_key", response_model=VpnReturnData)
async def create_key(key_data: CreateKeyClientBody, user_id: int = Depends(get_current_user_id)):
    if key_data.user_data.protocol == "vless":
        node_data = VlessClientInit(
            ux_url=key_data.node_data.ux_url,
            ux_pass=key_data.node_data.ux_pass,
            ux_username=key_data.node_data.ux_username,
            vless_inbound=key_data.node_data.vless_inbound,
            ip=key_data.node_data.ip,
            path=key_data.node_data.path,
        )
        vless_client = VlessPanelClient(panel_data=node_data)
        await vless_client.login()
        create_key = KeyData(user_id=user_id)

        try:
            key_vless = await vless_client.add_client(user_data=create_key)
            if not key_vless:
                raise HTTPException(status_code=500, detail="Don't create key")
            res = VpnReturnData(key_name=key_vless.key_name,
                                access_url=key_vless.access_url,
                                vless_uuid=key_vless.vless_uuid)
        finally:
            await vless_client.close()

    elif key_data.user_data.protocol == "outline":
        node_data = OutlineLoginData(out_cert=key_data.node_data.out_cert, out_url=key_data.node_data.out_url)
        create_key_data = OutlineCreateKey(user_id=user_id)
        outline_client = OutlinePanelClient()

        outline_client.login(session_data=node_data)
        key_out = await outline_client.outline_create_key(data=create_key_data)
        if not key_out:
            raise HTTPException(status_code=500, detail="Don't create key")
        
        res = VpnReturnData(key_name=key_out.key_name,
                            access_url=key_out.access_url,
                            server_key_id=key_out.server_key_id)
        
    return res

@router.post("/vpn/del_key")
async def del_key(key_data: DelKeyData, user_id: int = Depends(get_current_user_id)):
    if key_data.key_data.protocol == "vless":
        node_data = VlessClientInit(
            ux_url=key_data.node_data.ux_url,
            ux_pass=key_data.node_data.ux_pass,
            ux_username=key_data.node_data.ux_username,
            vless_inbound=key_data.node_data.vless_inbound,
            ip=key_data.node_data.ip,
            path=key_data.node_data.path,
        )
        vless_client = VlessPanelClient(panel_data=node_data)
        await vless_client.login()
        key_del_data = KeyDelData(vless_uuid=key_data.key_data.vless_uuid)
        
        try:
            res = await vless_client.del_client(key_data=key_del_data)
            if res == False:
                raise HTTPException(status_code=500, detail="don't del key")
        finally:
            await vless_client.close()

    elif key_data.key_data.protocol == "outline":
        node_data=OutlineLoginData(out_cert=key_data.node_data.out_cert, out_url=key_data.node_data.out_url)
        outline_client=OutlinePanelClient()

        outline_client.login(session_data=node_data)
        res = await outline_client.outline_del_key(server_key_id=key_data.key_data.server_key_id)
        if res == False:
            raise HTTPException(status_code=500, detail="don't del key")

    return {"status": "ok"}