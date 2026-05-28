import asyncio
from src.client.vless_panel_client import VlessPanelClient
from src.client.outline_client import OutlinePanelClient
from src.schemas.billing_schema import DelKeysData, DeleteKeys
from src.schemas.outline_schema import OutlineLoginData
from src.schemas.vless_schema import VlessClientInit, KeyDelData
from collections import defaultdict

class VlessCleaner:
    async def billing_del(self, billing_data: DelKeysData):
        vless_keys = defaultdict(list)
        outline_keys = defaultdict(list)

        for key in billing_data.keys_list:
            if key.protocol.lower() == "vless":
                vless_keys[key.node_id].append(key)

            elif key.protocol.lower() == "outline":
                outline_keys[key.node_id].append(key)

        for node_id, keys_list in outline_keys.items():
            node_config = next((n for n in billing_data.nodes_list if n.id == node_id), None)

            if not node_config:
                print(f"Error, not search Outline config: {node_id}")
                continue

            outline_client = OutlinePanelClient()
            login_data = OutlineLoginData(out_url=node_config.out_url, out_cert=node_config.out_cert)
            outline_client.login(session_data=login_data)
            
            print(f"Starting cleaning key outline on node {node_id}, keys: {len(keys_list)}")

            tasks = []
            for key in keys_list:
                key: DeleteKeys
                if key.server_key_id:
                    task = outline_client.outline_del_key(server_key_id=key.server_key_id)
                    tasks.append(task)

            await asyncio.gather(*tasks)

        for node_id, keys_list in vless_keys.items():
            node_config = next((n for n in billing_data.nodes_list if n.id == node_id), None)

            if not node_config:
                print(f"Error, not search Vless config: {node_id}")
                continue
            
            vless_init_data = VlessClientInit(
                ux_username=node_config.ux_username,
                ux_pass=node_config.ux_pass,
                ux_url=node_config.ux_url,
                vless_inbound=node_config.vless_inbound,
                ip=node_config.ip,
                path=node_config.path
            )
            vless_client = VlessPanelClient(panel_data=vless_init_data)
            await vless_client.login()

            tasks = []
            for key in keys_list:
                key: DeleteKeys
                if key.vless_uuid:
                    key_data = KeyDelData(vless_uuid=key.vless_uuid)
                    task = vless_client.del_client(key_data=key_data)
                    tasks.append(task)

            await asyncio.gather(*tasks)
            await vless_client.close()
            print(f"Vless node {node_id} successfully cleaned!")
            
